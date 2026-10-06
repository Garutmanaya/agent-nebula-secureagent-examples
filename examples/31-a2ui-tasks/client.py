"""Verify Example 31 native Task and A2UI artifact composition."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
from pathlib import Path

from a2a_client import request_report_task


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"


# -----------------------------------------------------------------------------
# Verification helpers
# -----------------------------------------------------------------------------

def a2ui_messages(task: dict) -> list[dict]:
    """Extract A2UI messages from the native Task artifact."""

    for artifact in task.get("artifacts", []):
        for part in artifact.get("parts", []):
            if part.get("media_type") == A2UI_MIME_TYPE:
                return part["data"]["messages"]

    raise AssertionError("Task does not contain an A2UI artifact")


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    task = await request_report_task(HERE)

    if task.get("status", {}).get("state") != "TASK_STATE_COMPLETED":
        raise AssertionError(f"unexpected Task state: {task.get('status')}")

    artifacts = task.get("artifacts", [])
    if len(artifacts) != 1 or artifacts[0].get("name") != "service-report":
        raise AssertionError(f"unexpected Task artifacts: {artifacts}")

    documents = a2ui_messages(task)
    create_surface = next(
        document["createSurface"]
        for document in documents
        if "createSurface" in document
    )
    if create_surface["surfaceId"] != "task-report-surface":
        raise AssertionError(f"unexpected A2UI surface: {create_surface}")

    print("PASS  native A2A Task completed")
    print("PASS  Task artifact contains application-owned A2UI DataPart")
    print("PASS  A2UI task-report-surface returned")
    print("RESULT: Example 31 A2UI + native Task verification passed")


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
