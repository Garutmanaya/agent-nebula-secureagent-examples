"""Browser bridge for A2UI Example 28."""

from __future__ import annotations

import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from a2a_client import request_surface


HERE = Path(__file__).resolve().parent
DIST = HERE.parents[1] / "examples" / "common" / "a2ui-web" / "dist"
A2UI_MIME_TYPE = "application/a2ui+json"


def extract_messages(message: dict) -> list[dict]:
    """Extract the A2UI document list from the native A2A Message."""

    return next(
        part["data"]["messages"]
        for part in message["parts"]
        if part.get("media_type") == A2UI_MIME_TYPE
    )


class Handler(SimpleHTTPRequestHandler):
    """Serve the shared renderer and bridge its A2UI request to native A2A."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/a2ui":
            message = asyncio.run(request_surface(HERE))
            body = json.dumps({"messages": extract_messages(message)}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()


if __name__ == "__main__":
    print("Browser validation: http://localhost:9128")
    ThreadingHTTPServer(("0.0.0.0", 9128), Handler).serve_forever()
