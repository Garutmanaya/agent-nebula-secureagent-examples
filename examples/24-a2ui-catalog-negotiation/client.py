"""Verify A2UI v1.0 catalog negotiation from AgentCard + turn metadata."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations

import asyncio
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
HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9024/"
A2UI_MIME_TYPE = "application/a2ui+json"
BASIC_CATALOG_ID = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
RICH_CATALOG_ID = "https://agentnebula.ai/catalogs/a2ui/rich/v1/catalog.json"

# -----------------------------------------------------------------------------
# AgentCard helpers
# -----------------------------------------------------------------------------
def _a2ui_capability(card) -> tuple[str, list[str]]:
    """Read the A2UI extension URI and v1.0 catalogs from the AgentCard."""
    matches: list[tuple[str, list[str]]] = []
    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        catalogs = params.get("v1.0", {}).get("supportedCatalogIds")
        if isinstance(catalogs, list):
            matches.append((extension.uri, [str(item) for item in catalogs]))
    if len(matches) != 1:
        raise AssertionError(f"expected one A2UI extension, got {matches}")
    return matches[0]

# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------
async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"), a2ui_config=config_path(HERE, "a2ui.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    card = await agent.resolve_agent_card(SERVER_URL)
    extension_uri, advertised = _a2ui_capability(card)
    if BASIC_CATALOG_ID not in advertised or RICH_CATALOG_ID not in advertised:
        raise AssertionError(f"unexpected advertised catalogs: {advertised}")
    print("PASS  Agent Card advertises Basic + Rich A2UI catalogs")

    metadata = ParseDict(
        {"a2uiRendererCapabilities": {"v1.0": {"supportedCatalogIds": [RICH_CATALOG_ID, BASIC_CATALOG_ID]}}},
        Struct(),
    )
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([extension_uri])]
        )
    )
    request = SendMessageRequest(message=new_text_message("show dashboard", role=Role.ROLE_USER), metadata=metadata)
    client = await agent.a2a_client(SERVER_URL)
    try:
        responses = [event async for event in client.send_message(request, context=context)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one A2A Message: {responses}")
        message = MessageToDict(responses[0].message, preserving_proto_field_name=True)
        part = next((p for p in message.get("parts", []) if p.get("media_type") == A2UI_MIME_TYPE), None)
        documents = part.get("data", {}).get("messages", []) if part else []
        create = documents[0].get("createSurface", {}) if documents else {}
        if create.get("catalogId") != RICH_CATALOG_ID:
            raise AssertionError(f"agent did not select preferred mutual catalog: {create}")
        print("PASS  A2UI extension activated through native a2a-sdk service parameters")
        print("PASS  renderer capabilities sent in A2A message metadata")
        print("PASS  agent selected preferred mutually supported Rich catalog")
        print("RESULT: Example 24 A2UI catalog negotiation verification passed")
    finally:
        await agent.close()

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
