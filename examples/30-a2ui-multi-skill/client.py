from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
from pathlib import Path

from a2a_client import discover_skills, request_surface


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
A2UI_MEDIA_TYPE = "application/a2ui+json"
RESULT_SURFACE_ID = "selected-skill-surface"


# -----------------------------------------------------------------------------
# Validation helpers
# -----------------------------------------------------------------------------

def extract_surface(message: dict) -> dict:
    """Extract the createSurface document from an A2A A2UI response."""

    documents = next(
        part["data"]["messages"]
        for part in message["parts"]
        if part.get("media_type") == A2UI_MEDIA_TYPE
    )

    return next(
        document["createSurface"]
        for document in documents
        if "createSurface" in document
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

async def main() -> None:
    """Validate AgentCard skills and skill-specific A2UI responses."""

    skills = await discover_skills(HERE)
    skill_ids = {skill["id"] for skill in skills}

    assert skill_ids == {"inventory", "traffic"}
    print("PASS  AgentCard advertises inventory and traffic skills")

    inventory = extract_surface(
        await request_surface(HERE, "inventory")
    )
    traffic = extract_surface(
        await request_surface(HERE, "traffic")
    )

    assert inventory["surfaceId"] == RESULT_SURFACE_ID
    assert traffic["surfaceId"] == RESULT_SURFACE_ID

    print("PASS  selected skills target the shared result surface")
    print("RESULT: Example 30 passed")


if __name__ == "__main__":
    asyncio.run(main())
