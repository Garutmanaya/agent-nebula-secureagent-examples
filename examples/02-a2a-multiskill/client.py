"""Verify Example 02 using the native a2a-sdk client and extension mechanism."""
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
SERVER_URL = "http://localhost:9002/"

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "multi-skill"}, "echo=multi-skill"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
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
    """Use the standard A2A extension activation and request metadata fields."""
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


# -----------------------------------------------------------------------------
# Example workflow
# -----------------------------------------------------------------------------


async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))

    client = await agent.a2a_client(SERVER_URL)
    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        advertised_skill_ids = {skill.id for skill in card.skills}
        expected_skill_ids = {case[0] for case in SKILL_CASES}
        if advertised_skill_ids != expected_skill_ids:
            raise AssertionError(f"unexpected advertised skills: {sorted(advertised_skill_ids)}")

        # Example 02 configures one A2A extension during SecureAgent agent creation.
        # The client consumes the URI advertised by the authoritative Agent Card;
        # it does not duplicate the configured extension URI.
        extensions = tuple(card.capabilities.extensions)
        if len(extensions) != 1:
            raise AssertionError(
                f"expected one configured A2A extension, received {len(extensions)}"
            )
        extension_uri = extensions[0].uri

        print(f"PASS  Agent Card skills: {', '.join(sorted(advertised_skill_ids))}")
        for skill_id, data, expected_text in SKILL_CASES:
            request, call_context = _skill_request(extension_uri, skill_id, data)
            responses = [
                event
                async for event in client.send_message(request, context=call_context)
            ]
            if len(responses) != 1 or not responses[0].HasField("message"):
                raise AssertionError(
                    f"{skill_id}: expected one native Message response: {responses}"
                )
            actual = get_message_text(responses[0].message, delimiter=" ")
            if actual != expected_text:
                raise AssertionError(
                    f"{skill_id}: expected {expected_text!r}, received {actual!r}"
                )
            print(f"PASS  JSON-RPC   {skill_id}")

        print(f"RESULT: {len(SKILL_CASES)}/{len(SKILL_CASES)} skill invocations passed")
    finally:
        await agent.close()


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
