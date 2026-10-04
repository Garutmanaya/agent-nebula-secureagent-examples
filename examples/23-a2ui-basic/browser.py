"""Browser validation host for Example 23.

The Python host uses the same native a2a-sdk client path as the CLI verifier. It
serves the A2UI documents unchanged to the shared browser renderer. Rendering
remains the responsibility of @a2ui/web_core and registered catalog adapters.
"""
from __future__ import annotations
import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from a2a_client import request_forecast

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DIST = REPO / "examples" / "common" / "a2ui-web" / "dist"

def extract_messages(message: dict) -> list[dict]:
    for part in message.get("parts", []):
        if part.get("media_type") == "application/a2ui+json":
            return part.get("data", {}).get("messages", [])
    raise ValueError("A2UI DataPart missing from A2A response")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/a2ui":
            try:
                message = asyncio.run(request_forecast(HERE))
                body = json.dumps({"messages": extract_messages(message)}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as exc:
                self.send_error(502, explain=str(exc))
            return
        super().do_GET()

if __name__ == "__main__":
    if not (DIST / "index.html").exists():
        raise SystemExit("Shared A2UI browser is not built. Run: make a2ui-web-build")
    print("Browser validation: http://localhost:9123")
    ThreadingHTTPServer(("0.0.0.0", 9123), Handler).serve_forever()
