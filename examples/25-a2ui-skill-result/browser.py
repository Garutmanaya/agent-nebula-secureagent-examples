"""Browser validation host for Example 25.

The host invokes both skills independently through native a2a-sdk and combines
only their returned A2UI protocol messages for display. The shared browser then
processes both surfaces without any Example-25-specific renderer code.
"""
from __future__ import annotations

import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from a2a_client import request_skill

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DIST = REPO / "examples" / "common" / "a2ui-web" / "dist"
A2UI_MIME_TYPE = "application/a2ui+json"


def extract_messages(message: dict) -> list[dict]:
    """Return A2UI protocol messages without translating their contents."""
    for part in message.get("parts", []):
        if part.get("media_type") == A2UI_MIME_TYPE:
            return part.get("data", {}).get("messages", [])
    raise ValueError("A2UI DataPart missing from A2A response")


async def load_surfaces() -> list[dict]:
    """Invoke both selected skills and preserve their provider-owned A2UI."""
    weather = await request_skill(HERE, "weather", "show weather")
    health = await request_skill(HERE, "system-health", "show system health")
    return [*extract_messages(weather), *extract_messages(health)]


class Handler(SimpleHTTPRequestHandler):
    """Serve the shared renderer and its Example 25 A2UI input."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/a2ui":
            try:
                body = json.dumps({"messages": asyncio.run(load_surfaces())}).encode()
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
    print("Browser validation: http://localhost:9125")
    ThreadingHTTPServer(("0.0.0.0", 9125), Handler).serve_forever()
