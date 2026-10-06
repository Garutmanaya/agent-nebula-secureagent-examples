"""CLI verification for native A2A transport of A2UI actions."""
from __future__ import annotations
import asyncio
from pathlib import Path
from a2a_client import request_surface, send_action
HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"

def extract_messages(message: dict) -> list[dict]:
    for part in message.get("parts", []):
        if part.get("media_type") == A2UI_MIME_TYPE:
            return part.get("data", {}).get("messages", [])
    raise AssertionError("A2UI DataPart missing")

async def main() -> None:
    initial = extract_messages(await request_surface(HERE))
    create = next(item["createSurface"] for item in initial if "createSurface" in item)
    assert create["surfaceId"] == "counter-surface" and create["sendDataModel"] is True
    print("PASS  application returned an interactive A2UI surface")
    action = {
        "name": "counter.increment",
        "surfaceId": "counter-surface",
        "sourceComponentId": "increment",
        "timestamp": "2026-10-04T12:00:00-04:00",
        "context": {"delta": 1},
    }
    updated = extract_messages(
        await send_action(
            HERE,
            action,
            {"version": "v1.0", "surfaces": {"counter-surface": {"count": 0}}},
        )
    )
    update = next(item["updateDataModel"] for item in updated if "updateDataModel" in item)
    assert update == {"surfaceId": "counter-surface", "path": "/count", "value": 1}
    print("PASS  renderer A2UI action reached the native AgentExecutor over A2A")
    print("PASS  synchronized renderer data model reached the application")
    print("PASS  application returned a native A2UI updateDataModel message")
    print("RESULT: Example 26 bidirectional A2UI action verification passed")

if __name__ == "__main__":
    asyncio.run(main())
