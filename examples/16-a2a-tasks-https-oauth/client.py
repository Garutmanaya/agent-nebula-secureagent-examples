"""Verify native A2A Message/Task execution after Nebula discovery over HTTPS + OAuth."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import annotations

import asyncio
from pathlib import Path

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import get_artifact_text, get_message_text, new_text_message
from a2a.types import GetTaskRequest, ListTasksRequest, Role, SendMessageRequest, TaskState
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PROVIDER_NAME = "Native A2A Tasks OAuth Agent"
DISCOVERY_QUERY = "generate reports"


# -----------------------------------------------------------------------------
# A2A request helpers
# -----------------------------------------------------------------------------

def _skill_call(extension_uri: str, skill_id: str) -> tuple[Struct, ClientCallContext]:
    metadata = ParseDict({extension_uri: {"skillId": skill_id}}, Struct())
    call_context = ClientCallContext(
        # Required for skill-level security: the client security resolver uses
        # this state value to select the advertised requirement for this skill.
        state={"agent_nebula.a2a.skill_id": skill_id},
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([extension_uri])]
        )
    )
    return metadata, call_context


async def _send(client, extension_uri: str, skill_id: str, text: str):
    metadata, call_context = _skill_call(extension_uri, skill_id)
    request = SendMessageRequest(
        message=new_text_message(text, role=Role.ROLE_USER),
        metadata=metadata,
    )
    responses = [event async for event in client.send_message(request, context=call_context)]
    if len(responses) != 1:
        raise AssertionError(f"{skill_id}: expected one aggregated response, got {len(responses)}")
    return responses[0]


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    # Same Agent Nebula Registry + OAuth profile used by Example 07.
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        nebula_config=config_path(HERE, "nebula.conf"),
    )
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))

    try:
        found = await agent.discover(query=DISCOVERY_QUERY)
        print(f"DISCOVERY: query={DISCOVERY_QUERY!r} returned {len(found)} agent(s)")
        if not found:
            raise AssertionError(f"Registry returned no provider for {DISCOVERY_QUERY!r}")

        provider = next((item for item in found if item.display_name == PROVIDER_NAME), found[0])
        print(f"SELECTED: name={provider.display_name!r} id={provider.agent_id!r}")

        # AgentCard is authoritative for the skill-selection extension URI.
        # SecureAgent applies the configured HTTPS trust + OAuth profile; operations
        # below remain native a2a-sdk APIs.
        agent_card_location = provider.require_agent_card_location()
        card = await agent.resolve_agent_card(agent_card_location)
        extensions = tuple(card.capabilities.extensions)
        if len(extensions) != 1:
            raise AssertionError(f"expected one skill-selection extension, got {len(extensions)}")
        extension_uri = extensions[0].uri
        client = await agent.a2a_client(agent_card_location)

        hello = await _send(client, extension_uri, "hello", "hello")
        if not hello.HasField("message"):
            raise AssertionError(f"hello did not return Message: {hello}")
        if get_message_text(hello.message) != "hello from native a2a-sdk":
            raise AssertionError(f"unexpected hello response: {hello.message}")
        print("PASS  HTTPS + OAuth hello -> native Message")

        report = await _send(client, extension_uri, "generate-reports", "generate reports")
        if not report.HasField("task"):
            raise AssertionError(f"generate-reports did not return Task: {report}")
        task = report.task
        if task.status.state != TaskState.TASK_STATE_COMPLETED:
            raise AssertionError(f"task did not complete: {TaskState.Name(task.status.state)}")

        artifacts = {artifact.name: get_artifact_text(artifact) for artifact in task.artifacts}
        expected = {
            "daily-report": "daily report ready",
            "weekly-report": "weekly report ready",
            "monthly-report": "monthly report ready",
        }
        if artifacts != expected:
            raise AssertionError(f"unexpected task artifacts: {artifacts}")
        print(f"PASS  HTTPS + OAuth generate-reports -> native Task {task.id}")
        print("PASS  Task contains daily/weekly/monthly artifacts")

        fetched = await client.get_task(GetTaskRequest(id=task.id, history_length=10))
        if fetched.id != task.id or fetched.status.state != TaskState.TASK_STATE_COMPLETED:
            raise AssertionError(f"get_task returned unexpected task: {fetched}")
        print("PASS  OAuth client.get_task()")

        listed = await client.list_tasks(
            ListTasksRequest(context_id=task.context_id, include_artifacts=True, page_size=10)
        )
        if task.id not in {item.id for item in listed.tasks}:
            raise AssertionError(f"list_tasks did not contain {task.id}")
        print("PASS  OAuth client.list_tasks()")

        print("RESULT: Registry discovery + HTTPS + OAuth + native Message/Task verification passed")
    finally:
        await agent.close()


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
