"""Browser validation endpoint for the secured A2UI example."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from a2a_client import A2UI_MIME_TYPE, request_surface


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
DIST = HERE.parents[1] / "examples" / "common" / "a2ui-web" / "dist"
HOST = "0.0.0.0"
PORT = 9133
A2UI_SURFACE_PATH = "/api/a2ui"


# -----------------------------------------------------------------------------
# A2UI helpers
# -----------------------------------------------------------------------------

def extract_a2ui_messages(message: dict) -> list[dict]:
    """Extract A2UI protocol messages from the native A2A Message."""

    for part in message["parts"]:
        if part.get("media_type") == A2UI_MIME_TYPE:
            return part["data"]["messages"]

    raise ValueError("native A2A response does not contain an A2UI DataPart")


# -----------------------------------------------------------------------------
# HTTP handler
# -----------------------------------------------------------------------------

class Handler(SimpleHTTPRequestHandler):
    """Serve the shared renderer and secured Example 33 A2UI endpoint."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def reply_json(self, payload: dict) -> None:
        """Return a JSON response."""

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        """Request the A2UI surface through HTTPS + OAuth protected A2A."""

        if urlparse(self.path).path != A2UI_SURFACE_PATH:
            super().do_GET()
            return

        try:
            result = asyncio.run(request_surface(HERE))
            messages = extract_a2ui_messages(result["message"])
            self.reply_json({"messages": messages})
        except Exception as exc:
            print(f"A2UI secured surface failed: {type(exc).__name__}: {exc}")
            self.send_error(502, explain=str(exc))


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

def main() -> None:
    """Run the Example 33 browser validation server."""

    print(f"Browser validation: http://localhost:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
