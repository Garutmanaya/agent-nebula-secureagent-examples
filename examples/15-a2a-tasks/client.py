"""Verify Example 15 with the native a2a-sdk client API."""
from __future__ import annotations

import asyncio
from pathlib import Path

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import get_artifact_text, get_message_text, new_text_message
from a2a.types import (
    GetTaskRequest,
    ListTasksRequest,
    Role,
    SendMessageRequest,
    TaskState,
)
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9015/"
SKILL_EXTENSION = "https://agentnebula.ai/extensions/a2a/skill-selection/v1"


def _skill_call(skill_id: str) -> tuple[Struct, ClientCallContext]:
    """Activate the Nebula skill-selection extension using native SDK fields."""
    metadata = ParseDict({SKILL_EXTENSION: {"skillId": skill_id}}, Struct())
    call_context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([SKILL_EXTENSION])]
        )
    )
    return metadata, call_context


async def _send(client, skill_id: str, text: str):
    metadata, call_context = _skill_call(skill_id)
    request = SendMessageRequest(
        message=new_text_message(text, role=Role.ROLE_USER),
        metadata=metadata,
    )
    responses = [event async for event in client.send_message(request, context=call_context)]
    if len(responses) != 1:
        raise AssertionError(f"{skill_id}: expected one aggregated response, got {len(responses)}")
    return responses[0]


async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    client = await agent.a2a_client(SERVER_URL)
    try:
        # Multi-skill proof #1: this skill owns an immediate native Message result.
        hello = await _send(client, "hello", "hello")
        if not hello.HasField("message"):
            raise AssertionError(f"hello did not return Message: {hello}")
        if get_message_text(hello.message) != "hello from native a2a-sdk":
            raise AssertionError(f"unexpected hello response: {hello.message}")
        print("PASS  hello -> native Message")

        # Multi-skill proof #2: this skill independently owns a native Task lifecycle.
        report = await _send(client, "generate-reports", "generate reports")
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
        print(f"PASS  generate-reports -> native Task {task.id}")
        print("PASS  Task contains daily/weekly/monthly artifacts")

        # STANDARD A2A CLIENT API: no SecureAgent task wrappers are used.
        fetched = await client.get_task(GetTaskRequest(id=task.id, history_length=10))
        if fetched.id != task.id or fetched.status.state != TaskState.TASK_STATE_COMPLETED:
            raise AssertionError(f"get_task returned unexpected task: {fetched}")
        print("PASS  client.get_task()")

        listed = await client.list_tasks(
            ListTasksRequest(context_id=task.context_id, include_artifacts=True, page_size=10)
        )
        if task.id not in {item.id for item in listed.tasks}:
            raise AssertionError(f"list_tasks did not contain {task.id}")
        print("PASS  client.list_tasks()")

        print("RESULT: Example 15 native A2A Message/Task verification passed")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
