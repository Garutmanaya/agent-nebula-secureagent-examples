"""Browser validation bridge for native A2A streaming + incremental A2UI."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from a2a_client import request_traffic_stream


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
DIST = HERE.parents[1] / "examples" / "common" / "a2ui-web" / "dist"
HOST = "0.0.0.0"
PORT = 9132
A2UI_SURFACE_PATH = "/api/a2ui"
NDJSON_MEDIA_TYPE = "application/x-ndjson"


# -----------------------------------------------------------------------------
# HTTP handler
# -----------------------------------------------------------------------------

class Handler(SimpleHTTPRequestHandler):
    """Serve the shared renderer and forward native A2A stream events live."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def start_stream(self) -> None:
        """Start a newline-delimited JSON response consumed incrementally."""

        self.send_response(200)
        self.send_header("Content-Type", NDJSON_MEDIA_TYPE)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    async def write_message(self, message: dict) -> None:
        """Write one A2UI protocol message immediately to the browser."""

        body = json.dumps({"message": message}).encode("utf-8") + b"\n"
        self.wfile.write(body)
        self.wfile.flush()

    def do_GET(self) -> None:
        """Forward each A2UI artifact message as its native stream event arrives."""

        if urlparse(self.path).path != A2UI_SURFACE_PATH:
            super().do_GET()
            return

        try:
            self.start_stream()
            result = asyncio.run(
                request_traffic_stream(HERE, on_message=self.write_message)
            )
            print(
                "A2UI stream: "
                f"events={result['eventKinds']} "
                f"messages={len(result['messages'])} "
                f"state={result['finalState']}"
            )
        except (BrokenPipeError, ConnectionResetError):
            print("A2UI streaming browser disconnected")
        except Exception as exc:
            # Headers may already be committed because streaming begins before
            # the native A2A operation completes. Log the actual stream error.
            print(f"A2UI streaming surface failed: {type(exc).__name__}: {exc}")


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

def main() -> None:
    """Run the Example 32 browser validation server."""

    print(f"Browser validation: http://localhost:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
