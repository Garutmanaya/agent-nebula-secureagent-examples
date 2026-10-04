"""Protocol-level verification for Example 25 multi-skill A2UI results."""
from __future__ import annotations

import asyncio
from pathlib import Path

from a2a_client import request_skill

HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"


def _surface(message: dict) -> dict:
    """Extract one A2UI createSurface document from a native A2A Message."""
    part = next(
        (
            item
            for item in message.get("parts", [])
            if item.get("media_type") == A2UI_MIME_TYPE
        ),
        None,
    )
    if part is None:
        raise AssertionError(f"A2UI DataPart missing: {message}")
    documents = part.get("data", {}).get("messages", [])
    if len(documents) != 1 or "createSurface" not in documents[0]:
        raise AssertionError(f"expected one createSurface document: {documents}")
    return documents[0]["createSurface"]


async def main() -> None:
    weather = _surface(await request_skill(HERE, "weather", "show weather"))
    health = _surface(await request_skill(HERE, "system-health", "show system health"))

    if weather.get("surfaceId") != "weather-surface":
        raise AssertionError(f"weather skill returned wrong surface: {weather}")
    if weather.get("dataModel", {}).get("temperature") != "72°F":
        raise AssertionError(f"weather skill returned wrong data: {weather}")

    if health.get("surfaceId") != "system-health-surface":
        raise AssertionError(f"system-health skill returned wrong surface: {health}")
    if health.get("dataModel", {}).get("status") != "Healthy":
        raise AssertionError(f"system-health skill returned wrong data: {health}")

    if weather.get("components") == health.get("components"):
        raise AssertionError("independent skills unexpectedly returned one presentation")

    print("PASS  weather skill -> native A2A Message -> application-owned A2UI")
    print("PASS  system-health skill -> native A2A Message -> independent A2UI")
    print("PASS  Nebula multi-skill dispatch did not control either A2UI result")
    print("RESULT: Example 25 A2UI skill-result verification passed")


if __name__ == "__main__":
    asyncio.run(main())
