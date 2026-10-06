"""OAuth-protected native A2A client for the combined A2UI example."""

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

SERVER_URL = "https://localhost:9034/"
A2UI_MIME_TYPE = "application/a2ui+json"
EXPECTED_SKILLS = {"service-report", "stream-traffic"}


# -----------------------------------------------------------------------------
# AgentCard extension discovery
# -----------------------------------------------------------------------------

def discover_extensions(card) -> tuple[str, str, list[str]]:
    """Discover A2UI, skill-selection, and catalog information from AgentCard."""

    a2ui_matches: list[tuple[str, list[str]]] = []
    dispatch_uris: list[str] = []

    for extension in card.capabilities.extensions:
        params = MessageToDict(extension.params) if extension.HasField("params") else {}
        catalogs = params.get("v1.0", {}).get("supportedCatalogIds")

        if catalogs is not None:
            a2ui_matches.append((extension.uri, list(catalogs)))
        else:
            dispatch_uris.append(extension.uri)

    if len(a2ui_matches) != 1 or len(dispatch_uris) != 1:
        raise AssertionError(
            "unexpected AgentCard extensions: "
            f"a2ui={a2ui_matches}, dispatch={dispatch_uris}"
        )

    a2ui_uri, supported_catalogs = a2ui_matches[0]
    if not supported_catalogs:
        raise AssertionError("A2UI extension advertises no supported catalogs")

    return a2ui_uri, dispatch_uris[0], supported_catalogs


def request_context(
    a2ui_uri: str,
    dispatch_uri: str,
    skill_id: str,
    supported_catalogs: list[str],
) -> tuple[Struct, ClientCallContext]:
    """Activate A2UI + skill selection using AgentCard-discovered values."""

    metadata = ParseDict(
        {
            "a2uiRendererCapabilities": {
                "v1.0": {
                    "supportedCatalogIds": supported_catalogs,
                }
            },
            dispatch_uri: {
                "skillId": skill_id,
            },
        },
        Struct(),
    )
    context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([a2ui_uri, dispatch_uri])]
        )
    )
    return metadata, context


# -----------------------------------------------------------------------------
# Native Task / streaming invocation
# -----------------------------------------------------------------------------

async def request_skill(
    here: Path,
    skill_id: str,
    on_message: Callable[[dict], Awaitable[None]] | None = None,
) -> dict:
    """Invoke one AgentCard-advertised skill and consume its native A2A events."""

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
        advertised_skills = {skill.id for skill in card.skills}
        if advertised_skills != EXPECTED_SKILLS:
            raise AssertionError(f"unexpected skills: {sorted(advertised_skills)}")
        if skill_id not in advertised_skills:
            raise AssertionError(f"skill is not advertised by AgentCard: {skill_id}")

        a2ui_uri, dispatch_uri, supported_catalogs = discover_extensions(card)
        metadata, context = request_context(
            a2ui_uri,
            dispatch_uri,
            skill_id,
            supported_catalogs,
        )
        request = SendMessageRequest(
            message=new_text_message(skill_id, role=Role.ROLE_USER),
            metadata=metadata,
        )
        client = await agent.a2a_client(SERVER_URL)

        event_kinds: list[str] = []
        messages: list[dict] = []
        final_state = None

        async for event in client.send_message(request, context=context):
            kind = event.WhichOneof("payload")
            event_kinds.append(kind)

            if kind == "artifact_update":
                artifact = MessageToDict(
                    event.artifact_update.artifact,
                    preserving_proto_field_name=True,
                )
                for part in artifact.get("parts", []):
                    if part.get("media_type") != A2UI_MIME_TYPE:
                        continue

                    for message in part.get("data", {}).get("messages", []):
                        messages.append(message)
                        if on_message is not None:
                            await on_message(message)

            elif kind == "status_update":
                final_state = event.status_update.status.state

        return {
            "eventKinds": event_kinds,
            "messages": messages,
            "finalState": (
                TaskState.Name(final_state)
                if final_state is not None
                else ""
            ),
            "supportedCatalogIds": supported_catalogs,
        }
    finally:
        await agent.close()
