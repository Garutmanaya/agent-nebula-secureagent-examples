"""Verify security + skills + Task/streaming + A2UI in one combined example."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
from pathlib import Path

from a2a_client import request_skill


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
COMPLETED = "TASK_STATE_COMPLETED"


# -----------------------------------------------------------------------------
# Validation helpers
# -----------------------------------------------------------------------------

def validate_catalogs(messages: list[dict], supported_catalogs: list[str]) -> None:
    """Verify every created surface uses an AgentCard-advertised catalog."""

    for message in messages:
        create_surface = message.get("createSurface")
        if create_surface is None:
            continue

        catalog_id = create_surface["catalogId"]
        if catalog_id not in supported_catalogs:
            raise AssertionError(
                f"surface catalog was not advertised by AgentCard: {catalog_id}"
            )


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    """Validate the complete secured multi-skill A2UI scenario."""

    report = await request_skill(HERE, "service-report")
    if report["finalState"] != COMPLETED or len(report["messages"]) != 1:
        raise AssertionError(f"service-report failed: {report}")
    validate_catalogs(report["messages"], report["supportedCatalogIds"])
    print("PASS  HTTPS + OAuth service-report -> native Task + A2UI artifact")

    traffic = await request_skill(HERE, "stream-traffic")
    creates = [
        message
        for message in traffic["messages"]
        if "createSurface" in message
    ]
    updates = [
        message
        for message in traffic["messages"]
        if "updateDataModel" in message
    ]

    if (
        traffic["finalState"] != COMPLETED
        or len(creates) != 1
        or len(updates) != 3
    ):
        raise AssertionError(f"stream-traffic failed: {traffic}")

    validate_catalogs(traffic["messages"], traffic["supportedCatalogIds"])
    print("PASS  HTTPS + OAuth stream-traffic -> native streaming + incremental A2UI")
    print("PASS  AgentCard-driven multi-skill dispatch and catalog negotiation")
    print("RESULT: Example 34 passed")


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
