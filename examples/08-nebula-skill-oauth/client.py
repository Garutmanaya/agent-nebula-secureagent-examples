"""Native A2A client for 08-nebula-skill-oauth."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import get_message_text
from a2a.types import Message, Part, Role, SendMessageRequest
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct, Value

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PROVIDER_NAME = 'Skill OAuth Registry Agent'
DISCOVERY_QUERY = 'hello'
AGENT_CARD_PATH = "/.well-known/agent-card.json"

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "registry"}, "echo=registry"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
)


# -----------------------------------------------------------------------------
# A2A request helpers
# -----------------------------------------------------------------------------

def _provider_base_url(agent_card_url: str) -> str:
    """Convert the Registry Agent Card location to its provider base URL."""
    if not agent_card_url.endswith(AGENT_CARD_PATH):
        raise AssertionError(f"unexpected Agent Card URL: {agent_card_url}")
    return agent_card_url.removesuffix(AGENT_CARD_PATH)


def _data_part(data: dict[str, object]) -> Part:
    """Build a standard A2A data part."""
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


def _skill_request(extension_uri: str, skill_id: str, data: dict[str, object]):
    """Build native A2A skill-selection metadata and call context."""
    metadata = ParseDict({extension_uri: {"skillId": skill_id}}, Struct())
    context = ClientCallContext(
        state={"agent_nebula.a2a.skill_id": skill_id},
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([extension_uri])]
        ),
    )
    request = SendMessageRequest(
        message=Message(
            role=Role.ROLE_USER,
            message_id=str(uuid.uuid4()),
            parts=[_data_part(data)],
        ),
        metadata=metadata,
    )
    return request, context


def _select_provider(found):
    """Select the named example provider from Registry discovery results."""
    if not found:
        raise AssertionError(f"Registry returned no provider for {DISCOVERY_QUERY!r}")
    return next((item for item in found if item.display_name == PROVIDER_NAME), found[0])


async def _invoke_skill(client, extension_uri: str, skill_id: str, data: dict[str, object]) -> str:
    """Invoke one skill through the native a2a-sdk Client."""
    request, context = _skill_request(extension_uri, skill_id, data)
    responses = [event async for event in client.send_message(request, context=context)]
    if len(responses) != 1 or not responses[0].HasField("message"):
        raise AssertionError(f"{skill_id}: expected one Message response: {responses}")
    return get_message_text(responses[0].message, delimiter=" ")


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    """Discover the provider, resolve its Agent Card, and invoke every skill."""
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        nebula_config=config_path(HERE, "nebula.conf"),
    )
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))

    try:
        # Registry discovery is Agent Nebula functionality outside the A2A protocol.
        provider = _select_provider(await agent.discover(query=DISCOVERY_QUERY))
        if not provider.agent_card_url:
            raise AssertionError("Registry result does not contain an Agent Card URL")
        print(f"PASS  Registry discovery: {provider.display_name}")

        provider_url = _provider_base_url(provider.agent_card_url)
        card = await agent.resolve_agent_card(provider_url)
        client = await agent.a2a_client(provider_url)

        advertised = {skill.id for skill in card.skills}
        expected = {case[0] for case in SKILL_CASES}
        if advertised != expected:
            raise AssertionError(f"unexpected advertised skills: {sorted(advertised)}")

        extensions = tuple(card.capabilities.extensions)
        if len(extensions) != 1:
            raise AssertionError(f"expected one skill-selection extension, got {len(extensions)}")
        extension_uri = extensions[0].uri

        for skill_id, data, expected_text in SKILL_CASES:
            actual = await _invoke_skill(client, extension_uri, skill_id, data)
            if actual != expected_text:
                raise AssertionError(f"{skill_id}: {actual!r} != {expected_text!r}")
            print(f"PASS  discovered provider {skill_id}")

        print("RESULT: Registry discovery and all native A2A invocations passed")
    finally:
        await agent.close()


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
