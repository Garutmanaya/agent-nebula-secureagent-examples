"""Native a2a-sdk client operations for Example 27."""

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
SKILL_EXTENSION = "https://agentnebula.ai/extensions/a2a/skill-selection/v1"
A2UI_EXTENSION = "https://a2ui.org/a2a-extension/a2ui/v1.0"
BASIC_CATALOG = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"


def _call_context() -> ClientCallContext:
    extensions = [SKILL_EXTENSION, A2UI_EXTENSION]
    parameters = ServiceParametersFactory.create([with_a2a_extensions(extensions)])
    return ClientCallContext(service_parameters=parameters)


def _request_metadata() -> Struct:
    return ParseDict({SKILL_EXTENSION: {"skillId": "contact-form"}}, Struct())


def _client_metadata(data_model: dict[str, Any] | None) -> Struct:
    metadata: dict[str, Any] = {
        "a2uiClientCapabilities": {
            "v1.0": {"supportedCatalogIds": [BASIC_CATALOG]}
        }
    }
    if data_model is not None:
        metadata["a2uiClientDataModel"] = data_model
    return ParseDict(metadata, Struct())


async def _send(here: Path, message) -> dict[str, Any]:
    agent = SecureAgent(config=config_path(here, "secureagent.conf"))
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(here, "a2aclient.conf"),
    )
    request = SendMessageRequest(message=message, metadata=_request_metadata())
    client = await agent.a2a_client(SERVER_URL)

    try:
        responses = [
            event
            async for event in client.send_message(request, context=_call_context())
        ]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one native A2A Message: {responses}")
        return MessageToDict(
            responses[0].message,
            preserving_proto_field_name=True,
        )
    finally:
        await agent.close()


async def request_surface(here: Path) -> dict[str, Any]:
    """Request the application's initial A2UI form surface."""
    message = new_text_message("show contact form", role=Role.ROLE_USER)
    message.metadata.CopyFrom(_client_metadata(None))
    return await _send(here, message)


async def submit_form(
    here: Path,
    action: dict[str, Any],
    data_model: dict[str, Any],
) -> dict[str, Any]:
    """Send the renderer-generated A2UI action and synchronized form state."""
    document = {"version": "v1.0", "action": action}
    message = new_message([a2ui_part([document])], role=Role.ROLE_USER)
    message.metadata.CopyFrom(_client_metadata(data_model))
    return await _send(here, message)
