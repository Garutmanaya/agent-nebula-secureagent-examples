"""OAuth-protected native A2A client for the A2UI security example."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

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

SERVER_URL = "https://aimlnode:9033/"
A2UI_MIME_TYPE = "application/a2ui+json"


# -----------------------------------------------------------------------------
# AgentCard / A2UI extension discovery
# -----------------------------------------------------------------------------

def discover_a2ui_extension(card) -> tuple[str, list[str]]:
    """Discover the A2UI extension URI and catalogs advertised by the AgentCard."""

    matches: list[tuple[str, list[str]]] = []

    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        catalogs = params.get("v1.0", {}).get("supportedCatalogIds")
        if catalogs is not None:
            matches.append((extension.uri, list(catalogs)))

    if len(matches) != 1:
        raise AssertionError(f"expected one A2UI extension, got {matches}")

    extension_uri, catalogs = matches[0]
    if not catalogs:
        raise AssertionError("A2UI extension advertises no supported catalogs")

    return extension_uri, catalogs


def request_context(
    a2ui_uri: str,
    supported_catalogs: list[str],
) -> tuple[Struct, ClientCallContext]:
    """Activate A2UI and advertise catalogs discovered from the AgentCard."""

    metadata = ParseDict(
        {
            "a2uiRendererCapabilities": {
                "v1.0": {
                    "supportedCatalogIds": supported_catalogs,
                }
            }
        },
        Struct(),
    )
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([a2ui_uri])]
        )
    )
    return metadata, context


# -----------------------------------------------------------------------------
# Native A2A request
# -----------------------------------------------------------------------------

async def request_surface(here: Path) -> dict:
    """Request an A2UI surface over the configured HTTPS + OAuth A2A client."""

    agent = SecureAgent(
        config=config_path(here, "secureagent.conf"),
        nebula_config=config_path(here, "nebula.conf"),
        a2ui_config=config_path(here, "a2ui.conf"),
    )
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(here, "a2aclient.conf"),
    )

    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        a2ui_uri, supported_catalogs = discover_a2ui_extension(card)
        metadata, context = request_context(a2ui_uri, supported_catalogs)

        request = SendMessageRequest(
            message=new_text_message(
                "show traffic chart",
                role=Role.ROLE_USER,
            ),
            metadata=metadata,
        )
        client = await agent.a2a_client(SERVER_URL)
        responses = [
            event
            async for event in client.send_message(
                request,
                context=context,
            )
        ]

        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(
                f"expected one native A2A Message response, got {responses}"
            )

        return {
            "message": MessageToDict(
                responses[0].message,
                preserving_proto_field_name=True,
            ),
            "supportedCatalogIds": supported_catalogs,
        }
    finally:
        await agent.close()
