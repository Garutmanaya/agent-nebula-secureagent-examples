"""Verify HTTPS + OAuth protection of a native A2A response carrying A2UI."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
from pathlib import Path

from a2a_client import A2UI_MIME_TYPE, request_surface


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent


# -----------------------------------------------------------------------------
# Validation helpers
# -----------------------------------------------------------------------------

def extract_a2ui_messages(message: dict) -> list[dict]:
    """Extract A2UI protocol messages from the native A2A Message."""

    for part in message["parts"]:
        if part.get("media_type") == A2UI_MIME_TYPE:
            return part["data"]["messages"]

    raise AssertionError("native A2A response does not contain an A2UI DataPart")


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    """Validate secured native A2A transport and the returned A2UI surface."""

    result = await request_surface(HERE)
    messages = extract_a2ui_messages(result["message"])
    create_surface = next(
        message["createSurface"]
        for message in messages
        if "createSurface" in message
    )

    if create_surface["surfaceId"] != "traffic-chart-surface":
        raise AssertionError(f"unexpected surface: {create_surface['surfaceId']}")

    if create_surface["catalogId"] not in result["supportedCatalogIds"]:
        raise AssertionError(
            "surface catalog was not advertised by the AgentCard: "
            f"{create_surface['catalogId']}"
        )

    chart = next(
        component
        for component in create_surface["components"]
        if component["component"] == "BarChart"
    )
    if chart["data"] != {"path": "/series"}:
        raise AssertionError(f"unexpected BarChart data binding: {chart['data']}")

    print("PASS  HTTPS + OAuth protected the native A2A request")
    print("PASS  A2UI extension and catalog were discovered from the AgentCard")
    print("PASS  Secured native A2A Message contains the A2UI BarChart")
    print("RESULT: Example 33 passed")


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
