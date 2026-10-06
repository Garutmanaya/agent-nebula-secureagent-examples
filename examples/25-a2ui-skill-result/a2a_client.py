"""Native a2a-sdk multi-skill invocation shared by CLI and browser clients."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
SERVER_URL = "http://localhost:9025/"

# -----------------------------------------------------------------------------
# AgentCard / request helpers
# -----------------------------------------------------------------------------
def _skill_extension_uri(card) -> str:
    """Find the non-A2UI dispatch extension advertised by the Agent Card."""
    candidates: list[str] = []
    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        if "supportedCatalogIds" not in params:
            candidates.append(extension.uri)
    if len(candidates) != 1:
        raise AssertionError(f"expected one skill-selection extension, got {candidates}")
    return candidates[0]


def _skill_call(extension_uri: str, skill_id: str) -> tuple[Struct, ClientCallContext]:
    """Activate the AgentCard-advertised skill-selection extension."""
    metadata = ParseDict({extension_uri: {"skillId": skill_id}}, Struct())
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([extension_uri])]
        )
    )
    return metadata, context


async def request_skill(here: Path, skill_id: str, text: str) -> dict:
    """Invoke one selected skill while leaving Message handling to a2a-sdk."""
    agent = SecureAgent(config=config_path(here, "secureagent.conf"), a2ui_config=config_path(here, "a2ui.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(here, "a2aclient.conf"))
    card = await agent.resolve_agent_card(SERVER_URL)
    extension_uri = _skill_extension_uri(card)
    metadata, context = _skill_call(extension_uri, skill_id)
    request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER), metadata=metadata)
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request, context=context)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"{skill_id}: expected one A2A Message: {responses}")
        return MessageToDict(responses[0].message, preserving_proto_field_name=True)
    finally:
        await agent.close()
