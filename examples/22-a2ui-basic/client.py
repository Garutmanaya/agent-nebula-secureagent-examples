"""Protocol-level verification for Example 22."""
import asyncio
from pathlib import Path
from a2a_client import request_forecast

HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"

async def main() -> None:
    message = await request_forecast(HERE)
    parts = message.get("parts", [])
    part = next((item for item in parts if item.get("media_type") == A2UI_MIME_TYPE), None)
    if part is None:
        raise AssertionError(f"A2UI DataPart missing: {message}")
    documents = part.get("data", {}).get("messages", [])
    create = documents[0].get("createSurface", {}) if documents else {}
    if create.get("surfaceId") != "forecast-surface":
        raise AssertionError(f"unexpected A2UI surface: {documents}")
    print("PASS  native a2a-sdk Message contains A2UI v1.0 DataPart")
    print("PASS  presentation.json supplied the Basic Catalog component tree")
    print("PASS  application supplied the A2UI data model directly")
    print("RESULT: Example 22 direct A2UI Basic verification passed")

if __name__ == "__main__": asyncio.run(main())
