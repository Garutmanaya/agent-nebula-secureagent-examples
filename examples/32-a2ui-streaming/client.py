"""Verify native A2A streaming carries incremental A2UI protocol messages."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
from pathlib import Path

from a2a_client import request_traffic_stream


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    result = await request_traffic_stream(HERE)
    messages = result["messages"]

    creates = [item for item in messages if "createSurface" in item]
    updates = [item for item in messages if "updateDataModel" in item]

    if len(creates) != 1:
        raise AssertionError(f"expected one createSurface message: {messages}")
    if len(updates) != 3:
        raise AssertionError(f"expected three updateDataModel messages: {messages}")
    if result["finalState"] != "TASK_STATE_COMPLETED":
        raise AssertionError(f"stream did not complete: {result}")

    final_series = updates[-1]["updateDataModel"]["value"]
    if [item["value"] for item in final_series] != [80, 50, 30]:
        raise AssertionError(f"unexpected final streaming data: {final_series}")

    print(f"PASS  native streaming events: {result['eventKinds']}")
    print("PASS  A2UI createSurface streamed through native Task artifact")
    print("PASS  three incremental A2UI updateDataModel messages streamed")
    print("PASS  final A2UI traffic data is 80 / 50 / 30")
    print("RESULT: Example 32 A2UI + native streaming verification passed")


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
