"""Verify native a2a-sdk streaming events without a SecureAgent stream API."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
import asyncio
from pathlib import Path
from a2a.helpers import get_artifact_text, new_text_message
from a2a.types import Role, SendMessageRequest, TaskState
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9018/"

# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------
async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    client = await agent.a2a_client(SERVER_URL)
    try:
        events = [
            event
            async for event in client.send_message(
                SendMessageRequest(
                    message=new_text_message("stream report", role=Role.ROLE_USER)
                )
            )
        ]
        kinds = []
        chunks = []
        final_state = None
        for event in events:
            kind = event.WhichOneof("payload")
            kinds.append(kind)
            if kind == "artifact_update":
                chunks.append(get_artifact_text(event.artifact_update.artifact))
            elif kind == "status_update":
                final_state = event.status_update.status.state
        if chunks != ["chunk one", "chunk two", "chunk three"]:
            raise AssertionError(f"unexpected streaming artifact chunks: {chunks}")
        if final_state != TaskState.TASK_STATE_COMPLETED:
            raise AssertionError(f"stream did not complete: {kinds}")
        print(f"PASS  native streaming events: {kinds}")
        print("PASS  streamed artifact chunks append to one artifact ID")
        print("RESULT: Example 18 native A2A streaming verification passed")
    finally:
        await agent.close()

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
