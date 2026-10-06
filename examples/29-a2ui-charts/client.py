"""Validate the A2UI surface returned by Example 29."""

import asyncio
from pathlib import Path

from a2a_client import request_surface


HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"


def messages(message: dict) -> list[dict]:
    """Extract A2UI protocol messages from the native A2A Message."""

    return next(
        part["data"]["messages"]
        for part in message["parts"]
        if part.get("media_type") == A2UI_MIME_TYPE
    )


async def main() -> None:
    documents = messages(await request_surface(HERE))
    create = next(
        document["createSurface"]
        for document in documents
        if "createSurface" in document
    )
    assert create["surfaceId"] == "traffic-chart-surface"
    print("PASS  A2UI chart surface returned over native A2A")
    print("RESULT: Example 29 passed")


if __name__ == "__main__":
    asyncio.run(main())
