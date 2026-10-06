"""Native a2a-sdk multi-skill invocation with AgentCard-negotiated A2UI."""
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
BASIC_CATALOG_ID = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"

# -----------------------------------------------------------------------------
# AgentCard / request helpers
# -----------------------------------------------------------------------------
def _extension_uris(card) -> tuple[str, str]:
    """Discover A2UI and skill-selection extensions from AgentCard semantics."""
    a2ui: list[str] = []
    dispatch: list[str] = []
    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        if "supportedCatalogIds" in params.get("v1.0", {}):
            a2ui.append(extension.uri)
        else:
            dispatch.append(extension.uri)
    if len(a2ui) != 1 or len(dispatch) != 1:
        raise AssertionError(f"unexpected AgentCard extensions: a2ui={a2ui}, dispatch={dispatch}")
    return dispatch[0], a2ui[0]


def _request_context(dispatch_uri: str, a2ui_uri: str, skill_id: str) -> tuple[Struct, ClientCallContext]:
    """Activate both advertised extensions and attach their turn metadata."""
    metadata = ParseDict(
        {
            dispatch_uri: {"skillId": skill_id},
            "a2uiRendererCapabilities": {"v1.0": {"supportedCatalogIds": [BASIC_CATALOG_ID]}},
        },
        Struct(),
    )
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([dispatch_uri, a2ui_uri])]
        )
    )
    return metadata, context


async def request_skill(here: Path, skill_id: str, text: str) -> dict:
    """Invoke one selected skill through native a2a-sdk with A2UI enabled."""
    agent = SecureAgent(config=config_path(here, "secureagent.conf"), a2ui_config=config_path(here, "a2ui.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(here, "a2aclient.conf"))
    card = await agent.resolve_agent_card(SERVER_URL)
    dispatch_uri, a2ui_uri = _extension_uris(card)
    metadata, context = _request_context(dispatch_uri, a2ui_uri, skill_id)
    request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER), metadata=metadata)
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request, context=context)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"{skill_id}: expected one A2A Message: {responses}")
        return MessageToDict(responses[0].message, preserving_proto_field_name=True)
    finally:
        await agent.close()
