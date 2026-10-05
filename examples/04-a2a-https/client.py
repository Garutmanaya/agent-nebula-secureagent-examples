"""Verify every skill over certificate-verified HTTPS."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
import uuid
from pathlib import Path

from a2a.client import Client, ClientCallContext
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
SERVER_URL = 'https://localhost:9004/'
SKILL_CASES = (
    ('hello', {'name': 'Agent Nebula'}, 'hello from SecureAgent'),
    ('echo', {'value': 'https'}, 'echo=https'),
    ('add', {'a': 7, 'b': 5}, 'sum=12'),
)


# -----------------------------------------------------------------------------
# A2A request helpers
# -----------------------------------------------------------------------------


def _data_part(data: dict[str, object]) -> Part:
    """Convert a Python mapping to a native A2A DataPart."""
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


def _skill_request(
    extension_uri: str,
    skill_id: str,
    data: dict[str, object],
) -> tuple[SendMessageRequest, ClientCallContext]:
    """Build a request that activates the advertised skill-selection extension."""
    metadata = ParseDict({extension_uri: {"skillId": skill_id}}, Struct())
    call_context = ClientCallContext(
        service_parameters=ServiceParametersFactory.create(
            [with_a2a_extensions([extension_uri])]
        )
    )
    request = SendMessageRequest(
        message=Message(
            role=Role.ROLE_USER,
            message_id=str(uuid.uuid4()),
            parts=[_data_part(data)],
        ),
        metadata=metadata,
    )
    return request, call_context


async def _invoke_skill(
    client: Client,
    extension_uri: str,
    skill_id: str,
    data: dict[str, object],
) -> str:
    """Invoke one skill and return the text from its single Message response."""
    request, call_context = _skill_request(extension_uri, skill_id, data)
    responses = [
        event
        async for event in client.send_message(request, context=call_context)
    ]
    if len(responses) != 1 or not responses[0].HasField("message"):
        raise AssertionError(
            f"{skill_id}: expected one Message response: {responses}"
        )
    return get_message_text(responses[0].message, delimiter=" ")


# -----------------------------------------------------------------------------
# SecureAgent client configuration
# -----------------------------------------------------------------------------


def _configured_client(configuration_file: str) -> SecureAgent:
    """Create a SecureAgent client facade for one transport configuration."""
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(HERE, configuration_file),
    )
    return agent


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------

async def main() -> None:
    """Verify every skill through the certificate-verified HTTPS interface."""
    agent = _configured_client("a2aclient.conf")
    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        if not card.supported_interfaces or not all(
            interface.url.startswith("https://")
            for interface in card.supported_interfaces
        ):
            raise AssertionError("Agent Card must advertise HTTPS interfaces only")

        extension_uri = card.capabilities.extensions[0].uri
        client = await agent.a2a_client(SERVER_URL)

        for skill_id, payload, expected_text in SKILL_CASES:
            actual_text = await _invoke_skill(
                client, extension_uri, skill_id, payload
            )
            if actual_text != expected_text:
                raise AssertionError(
                    f"{skill_id}: {actual_text!r} != {expected_text!r}"
                )
            print(f"PASS  HTTPS      {skill_id}")
    finally:
        await agent.close()


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
