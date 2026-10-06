from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from pathlib import Path

from a2a.client import ClientCallContext
from a2a.client.service_parameters import (
    ServiceParametersFactory,
    with_a2a_extensions,
)
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from agent_nebula_secureagent import SecureAgent
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.struct_pb2 import Struct

from examples.example_paths import config_path


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

RICH_CATALOG_ID = (
    "https://agentnebula.ai/catalogs/a2ui/rich/v1/catalog.json"
)
SERVER_URL = "http://localhost:9030/"


# -----------------------------------------------------------------------------
# AgentCard discovery
# -----------------------------------------------------------------------------

def discover_extensions(card, need_dispatch: bool = False):
    """Discover A2UI and skill-selection extensions from the AgentCard."""

    a2ui_extensions = []
    other_extensions = []

    for extension in card.capabilities.extensions:
        params = (
            MessageToDict(extension.params)
            if extension.HasField("params")
            else {}
        )

        supported_catalogs = params.get("v1.0", {}).get(
            "supportedCatalogIds"
        )

        if supported_catalogs is not None:
            a2ui_extensions.append(extension.uri)
        else:
            other_extensions.append(extension.uri)

    if len(a2ui_extensions) != 1:
        raise AssertionError(
            f"unexpected A2UI extensions: {a2ui_extensions}"
        )

    if need_dispatch and len(other_extensions) != 1:
        raise AssertionError(
            "unexpected non-A2UI extensions: "
            f"{other_extensions}"
        )

    dispatch_uri = (
        other_extensions[0]
        if need_dispatch
        else None
    )

    return a2ui_extensions[0], dispatch_uri


async def discover_skills(here: Path) -> list[dict]:
    """Return skills advertised by the server AgentCard."""

    agent = SecureAgent(
        config=config_path(here, "secureagent.conf"),
        a2ui_config=config_path(here, "a2ui.conf"),
    )
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(here, "a2aclient.conf"),
    )

    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        skills = MessageToDict(card).get("skills", [])

        return [
            {
                "id": skill["id"],
                "name": skill.get("name", skill["id"]),
                "description": skill.get("description", ""),
            }
            for skill in skills
        ]
    finally:
        await agent.close()


# -----------------------------------------------------------------------------
# A2A skill invocation
# -----------------------------------------------------------------------------

async def request_surface(here: Path, skill_id: str) -> dict:
    """Invoke one selected skill with A2UI renderer capabilities."""

    agent = SecureAgent(
        config=config_path(here, "secureagent.conf"),
        a2ui_config=config_path(here, "a2ui.conf"),
    )
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(here, "a2aclient.conf"),
    )

    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        a2ui_uri, dispatch_uri = discover_extensions(
            card,
            need_dispatch=True,
        )

        metadata = ParseDict(
            {
                dispatch_uri: {
                    "skillId": skill_id,
                },
                "a2uiRendererCapabilities": {
                    "v1.0": {
                        "supportedCatalogIds": [RICH_CATALOG_ID],
                    }
                },
            },
            Struct(),
        )

        request = SendMessageRequest(
            message=new_text_message(
                f"show {skill_id}",
                role=Role.ROLE_USER,
            ),
            metadata=metadata,
        )

        context = ClientCallContext(
            service_parameters=ServiceParametersFactory.create(
                [
                    with_a2a_extensions(
                        [dispatch_uri, a2ui_uri]
                    )
                ]
            )
        )

        client = await agent.a2a_client(SERVER_URL)
        responses = [
            event
            async for event in client.send_message(
                request,
                context=context,
            )
        ]

        return MessageToDict(
            responses[0].message,
            preserving_proto_field_name=True,
        )
    finally:
        await agent.close()
