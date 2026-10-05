"""Verify native A2A artifact creation and persisted retrieval."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
import asyncio
from pathlib import Path
from a2a.helpers import get_artifact_text, new_text_message
from a2a.types import GetTaskRequest, Role, SendMessageRequest, TaskState
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9017/"

# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------
async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(SendMessageRequest(message=new_text_message("build artifacts", role=Role.ROLE_USER)))]
        task = responses[-1].task
        if task.status.state != TaskState.TASK_STATE_COMPLETED:
            raise AssertionError("artifact task did not complete")
        expected = {"first-artifact": "artifact one", "second-artifact": "artifact two"}
        actual = {item.name: get_artifact_text(item) for item in task.artifacts}
        if actual != expected:
            raise AssertionError(f"unexpected artifacts: {actual}")
        if {item.artifact_id for item in task.artifacts} != {"artifact-one", "artifact-two"}:
            raise AssertionError("artifact IDs were not preserved")
        print("PASS  native Artifact IDs, names, Parts")
        fetched = await client.get_task(GetTaskRequest(id=task.id, history_length=10))
        persisted = {item.name: get_artifact_text(item) for item in fetched.artifacts}
        if persisted != expected:
            raise AssertionError(f"TaskStore did not persist artifacts: {persisted}")
        print("PASS  artifacts persisted through native TaskStore/get_task()")
        print("RESULT: Example 17 native A2A artifacts verification passed")
    finally:
        await agent.close()

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
