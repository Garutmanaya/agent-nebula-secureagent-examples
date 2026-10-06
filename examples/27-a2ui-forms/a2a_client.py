"""Native a2a-sdk transport for Example 27; extension URIs come from AgentCard."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
from pathlib import Path
from typing import Any
from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import new_message, new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.struct_pb2 import Struct
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
from a2ui_transport import a2ui_part

SERVER_URL = "http://localhost:9027/"
BASIC_CATALOG_ID = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"

# -----------------------------------------------------------------------------
# AgentCard discovery
# -----------------------------------------------------------------------------
def _extensions(card) -> tuple[str, str]:
    a2ui = []
    other = []
    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        if "supportedCatalogIds" in params.get("v1.0", {}):
            a2ui.append(extension.uri)
        else:
            other.append(extension.uri)
    if len(a2ui) != 1 or len(other) != 1:
        raise AssertionError(f"expected A2UI + skill-selection extensions, got a2ui={a2ui}, other={other}")
    return a2ui[0], other[0]

async def _send(here: Path, message, data_model: dict[str, Any] | None = None) -> dict[str, Any]:
    agent = SecureAgent(config=config_path(here, "secureagent.conf"), a2ui_config=config_path(here, "a2ui.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(here, "a2aclient.conf"))
    card = await agent.resolve_agent_card(SERVER_URL)
    a2ui_uri, dispatch_uri = _extensions(card)
    request_metadata = {
        dispatch_uri: {"skillId": "contact-form"},
        "a2uiRendererCapabilities": {"v1.0": {"supportedCatalogIds": [BASIC_CATALOG_ID]}},
    }
    if data_model is not None:
        request_metadata["a2uiClientDataModel"] = data_model
    request = SendMessageRequest(message=message, metadata=ParseDict(request_metadata, Struct()))
    context = ClientCallContext(service_parameters=ServiceParametersFactory.create([with_a2a_extensions([dispatch_uri, a2ui_uri])]))
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request, context=context)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one native A2A Message: {responses}")
        return MessageToDict(responses[0].message, preserving_proto_field_name=True)
    finally:
        await agent.close()

async def request_surface(here: Path) -> dict[str, Any]:
    return await _send(here, new_text_message("show contact-form", role=Role.ROLE_USER))

async def send_action(here: Path, action: dict[str, Any], data_model: dict[str, Any]) -> dict[str, Any]:
    return await _send(here, new_message([a2ui_part([{"version": "v1.0", "action": action}])], role=Role.ROLE_USER), data_model)

submit_form = send_action
