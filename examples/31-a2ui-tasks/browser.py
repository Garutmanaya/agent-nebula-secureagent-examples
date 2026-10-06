"""Browser validation bridge for the native A2A Task + A2UI example."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from a2a_client import request_report_task
from presentation import load_presentation


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
DIST = HERE.parents[1] / "examples" / "common" / "a2ui-web" / "dist"
HOST = "0.0.0.0"
PORT = 9131
A2UI_MIME_TYPE = "application/a2ui+json"
A2UI_SURFACE_PATH = "/api/a2ui"
TASK_STATUS_PRESENTATION = HERE / "task-status.json"


# -----------------------------------------------------------------------------
# Task artifact helpers
# -----------------------------------------------------------------------------

def extract_a2ui_messages(task: dict) -> list[dict]:
    """Extract A2UI protocol messages from the completed Task artifact."""

    for artifact in task.get("artifacts", []):
        for part in artifact.get("parts", []):
            if part.get("media_type") == A2UI_MIME_TYPE:
                return part["data"]["messages"]

    raise ValueError("completed Task does not contain an A2UI artifact")


def build_task_status_message(task: dict) -> dict:
    """Build a validation surface from the actual native A2A Task metadata."""

    artifacts = task.get("artifacts", [])
    artifact_name = artifacts[0].get("name", "") if artifacts else ""
    task_data = {
        "taskId": task.get("id", ""),
        "state": task.get("status", {}).get("state", ""),
        "artifact": artifact_name,
    }
    return load_presentation(TASK_STATUS_PRESENTATION, task_data)


# -----------------------------------------------------------------------------
# HTTP handler
# -----------------------------------------------------------------------------

class Handler(SimpleHTTPRequestHandler):
    """Serve the shared renderer and bridge its initial request to native A2A."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def reply_json(self, payload: dict) -> None:
        """Return a JSON response to the shared browser renderer."""

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        """Request the native Task and render its A2UI artifact."""

        if urlparse(self.path).path != A2UI_SURFACE_PATH:
            super().do_GET()
            return

        try:
            task = asyncio.run(request_report_task(HERE))
            messages = [build_task_status_message(task)]
            messages.extend(extract_a2ui_messages(task))
            self.reply_json({"messages": messages})
        except Exception as exc:
            print(f"A2UI Task surface failed: {type(exc).__name__}: {exc}")
            self.send_error(502, explain=str(exc))


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

def main() -> None:
    """Run the Example 31 browser validation server."""

    print(f"Browser validation: http://localhost:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
