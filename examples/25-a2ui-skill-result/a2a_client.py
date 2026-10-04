"""Native a2a-sdk multi-skill invocation shared by CLI and browser clients."""
from __future__ import annotations

from pathlib import Path

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.struct_pb2 import Struct

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

SERVER_URL = "http://localhost:9025/"
SKILL_EXTENSION = "https://agentnebula.ai/extensions/a2a/skill-selection/v1"


def _skill_call(skill_id: str) -> tuple[Struct, ClientCallContext]:
    """Select one advertised skill using the Agent Nebula A2A extension."""
    metadata = ParseDict({SKILL_EXTENSION: {"skillId": skill_id}}, Struct())
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([SKILL_EXTENSION])]
        )
    )
    return metadata, context


async def request_skill(here: Path, skill_id: str, text: str) -> dict:
    """Invoke one skill while leaving Message handling to native a2a-sdk."""
    agent = SecureAgent(config=config_path(here, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(here, "a2aclient.conf"))
    metadata, context = _skill_call(skill_id)
    request = SendMessageRequest(
        message=new_text_message(text, role=Role.ROLE_USER),
        metadata=metadata,
    )
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request, context=context)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"{skill_id}: expected one A2A Message: {responses}")
        return MessageToDict(
            responses[0].message,
            preserving_proto_field_name=True,
        )
    finally:
        await agent.close()
