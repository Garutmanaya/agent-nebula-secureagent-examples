"""Native a2a-sdk invocation with AgentCard-negotiated A2UI v1.0."""
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
SERVER_URL = "http://localhost:9023/"

# -----------------------------------------------------------------------------
# AgentCard / request helpers
# -----------------------------------------------------------------------------
def _a2ui_capability(card) -> tuple[str, list[str]]:
    """Read the A2UI extension URI and catalogs advertised by the AgentCard."""

    matches: list[tuple[str, list[str]]] = []
    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        catalogs = params.get("v1.0", {}).get("supportedCatalogIds")
        if isinstance(catalogs, list):
            matches.append((extension.uri, [str(item) for item in catalogs]))

    if len(matches) != 1:
        raise AssertionError(f"expected one A2UI extension, got {matches}")

    extension_uri, catalogs = matches[0]
    if not catalogs:
        raise AssertionError("A2UI extension advertises no supported catalogs")

    return extension_uri, catalogs


async def request_dashboard(here: Path, text: str = "show weather dashboard") -> dict:
    """Invoke the skill with A2UI activated through native a2a-sdk."""
    agent = SecureAgent(
        config=config_path(here, "secureagent.conf"),
        a2ui_config=config_path(here, "a2ui.conf"),
    )
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(here, "a2aclient.conf"),
    )
    card = await agent.resolve_agent_card(SERVER_URL)
    extension_uri, supported_catalogs = _a2ui_capability(card)
    metadata = ParseDict(
        {"a2uiRendererCapabilities": {"v1.0": {"supportedCatalogIds": supported_catalogs}}},
        Struct(),
    )
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([extension_uri])]
        )
    )
    request = SendMessageRequest(
        message=new_text_message(text, role=Role.ROLE_USER),
        metadata=metadata,
    )
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [
            event async for event in client.send_message(request, context=context)
        ]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one A2A Message: {responses}")
        return MessageToDict(responses[0].message, preserving_proto_field_name=True)
    finally:
        await agent.close()
