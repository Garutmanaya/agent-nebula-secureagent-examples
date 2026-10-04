"""CLI verification for A2UI form binding and submission over native A2A."""

from __future__ import annotations

import asyncio
from pathlib import Path

from a2a_client import request_surface, submit_form

HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"
SURFACE_ID = "contact-form-surface"


def extract_messages(message: dict) -> list[dict]:
    """Extract A2UI messages from the native A2A response."""
    for part in message.get("parts", []):
        if part.get("media_type") == A2UI_MIME_TYPE:
            return part.get("data", {}).get("messages", [])
    raise AssertionError("A2UI DataPart missing")


async def main() -> None:
    initial = extract_messages(await request_surface(HERE))
    create = next(item["createSurface"] for item in initial if "createSurface" in item)
    components = {item["id"]: item for item in create["components"]}

    assert create["surfaceId"] == SURFACE_ID
    assert create["sendDataModel"] is True
    assert components["name_input"]["component"] == "TextField"
    assert components["name_input"]["value"] == {"path": "/name"}
    assert components["email_input"]["value"] == {"path": "/email"}
    print("PASS  presentation.json defines two-way A2UI form bindings")

    action = {
        "name": "contact.submit",
        "surfaceId": SURFACE_ID,
        "sourceComponentId": "submit_button",
        "timestamp": "2026-10-04T14:00:00-04:00",
        "context": {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
        },
    }
    data_model = {
        "version": "v1.0",
        "surfaces": {
            SURFACE_ID: {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "result": "Waiting for form submission.",
            }
        },
    }

    updated = extract_messages(await submit_form(HERE, action, data_model))
    update = next(item["updateDataModel"] for item in updated if "updateDataModel" in item)
    assert update == {
        "surfaceId": SURFACE_ID,
        "path": "/result",
        "value": "Submitted: Ada Lovelace <ada@example.com>",
    }

    print("PASS  submitted form values reached the native AgentExecutor over A2A")
    print("PASS  synchronized renderer data model reached the application")
    print("PASS  application returned an incremental A2UI form result update")
    print("RESULT: Example 27 A2UI form verification passed")


if __name__ == "__main__":
    asyncio.run(main())
