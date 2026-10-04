"""Native a2a-sdk invocation shared by Example 24 CLI and browser clients."""
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

SERVER_URL = "http://localhost:9024/"
SKILL_EXTENSION = "https://agentnebula.ai/extensions/a2a/skill-selection/v1"


async def request_dashboard(here: Path) -> dict:
    """Request the dashboard through SecureAgent's configured native A2A client."""
    agent = SecureAgent(config=config_path(here, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(here, "a2aclient.conf"))

    metadata = ParseDict(
        {SKILL_EXTENSION: {"skillId": "weather-dashboard"}},
        Struct(),
    )
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([SKILL_EXTENSION])]
        )
    )
    request = SendMessageRequest(
        message=new_text_message("show weather dashboard", role=Role.ROLE_USER),
        metadata=metadata,
    )
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request, context=context)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one A2A Message: {responses}")
        return MessageToDict(
            responses[0].message,
            preserving_proto_field_name=True,
        )
    finally:
        await agent.close()
