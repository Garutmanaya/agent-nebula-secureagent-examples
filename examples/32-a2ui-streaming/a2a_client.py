"""Native a2a-sdk streaming client for the A2UI streaming example."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from collections.abc import Awaitable, Callable
from pathlib import Path

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest, TaskState
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.struct_pb2 import Struct

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

SERVER_URL = "http://localhost:9032/"
A2UI_MIME_TYPE = "application/a2ui+json"


# -----------------------------------------------------------------------------
# AgentCard / A2UI extension discovery
# -----------------------------------------------------------------------------

def discover_a2ui_extension(card) -> tuple[str, list[str]]:
    """Discover the A2UI extension from its advertised semantic parameters."""

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


def request_context(
    a2ui_uri: str,
    supported_catalogs: list[str],
) -> tuple[Struct, ClientCallContext]:
    """Activate A2UI and advertise the Rich renderer capability."""

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
# Native streaming request
# -----------------------------------------------------------------------------

async def request_traffic_stream(
    here: Path,
    on_message: Callable[[dict], Awaitable[None]] | None = None,
) -> dict:
    """Consume native streaming events and optionally forward each A2UI message."""

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
    a2ui_uri, supported_catalogs = discover_a2ui_extension(card)
    metadata, context = request_context(a2ui_uri, supported_catalogs)
    request = SendMessageRequest(
        message=new_text_message("stream traffic", role=Role.ROLE_USER),
        metadata=metadata,
    )
    client = await agent.a2a_client(SERVER_URL)

    event_kinds: list[str] = []
    messages: list[dict] = []
    final_state = None

    try:
        async for event in client.send_message(request, context=context):
            kind = event.WhichOneof("payload")
            event_kinds.append(kind)

            if kind == "artifact_update":
                artifact = MessageToDict(
                    event.artifact_update.artifact,
                    preserving_proto_field_name=True,
                )
                for part in artifact.get("parts", []):
                    if part.get("media_type") == A2UI_MIME_TYPE:
                        for message in part.get("data", {}).get("messages", []):
                            messages.append(message)
                            if on_message is not None:
                                await on_message(message)

            elif kind == "status_update":
                final_state = event.status_update.status.state
    finally:
        await agent.close()

    return {
        "eventKinds": event_kinds,
        "messages": messages,
        "finalState": TaskState.Name(final_state) if final_state is not None else "",
    }
