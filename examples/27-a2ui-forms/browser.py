"""Browser bridge for real A2UI form validation in Example 27."""

from __future__ import annotations

import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from a2a_client import request_surface, submit_form

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DIST = REPO / "examples" / "common" / "a2ui-web" / "dist"
A2UI_MIME_TYPE = "application/a2ui+json"


def extract_messages(message: dict) -> list[dict]:
    """Extract the provider's A2UI messages from the native A2A response."""
    for part in message.get("parts", []):
        if part.get("media_type") == A2UI_MIME_TYPE:
            return part.get("data", {}).get("messages", [])
    raise ValueError("A2UI DataPart missing from A2A response")


class Handler(SimpleHTTPRequestHandler):
    """Serve the shared renderer and bridge browser interactions to native A2A."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def _json_response(self, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/a2ui":
            try:
                message = asyncio.run(request_surface(HERE))
                self._json_response({"messages": extract_messages(message)})
            except Exception as exc:
                self.send_error(502, explain=str(exc))
            return
        super().do_GET()

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/a2ui/action":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            message = asyncio.run(
                submit_form(
                    HERE,
                    payload["action"],
                    payload.get("dataModel", {}),
                )
            )
            self._json_response({"messages": extract_messages(message)})
        except Exception as exc:
            self.send_error(502, explain=str(exc))


if __name__ == "__main__":
    if not (DIST / "index.html").exists():
        raise SystemExit("Shared A2UI browser is not built. Run: make a2ui-web-build")

    print("Browser validation: http://localhost:9127")
    ThreadingHTTPServer(("0.0.0.0", 9127), Handler).serve_forever()
