"""Verify every skill over certificate-verified HTTPS."""
import asyncio
from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent


import uuid

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import get_message_text
from a2a.types import Message, Part, Role, SendMessageRequest
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct, Value


def _data_part(data: dict[str, object]) -> Part:
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


def _skill_request(extension_uri: str, skill_id: str, data: dict[str, object]):
    metadata = ParseDict({extension_uri: {"skillId": skill_id}}, Struct())
    context = ClientCallContext(
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
    return request, context


async def _invoke(client, extension_uri: str, skill_id: str, data: dict[str, object]) -> str:
    request, context = _skill_request(extension_uri, skill_id, data)
    responses = [event async for event in client.send_message(request, context=context)]
    if len(responses) != 1 or not responses[0].HasField("message"):
        raise AssertionError(f"{skill_id}: expected one Message response: {responses}")
    return get_message_text(responses[0].message, delimiter=" ")

HERE = Path(__file__).resolve().parent
SERVER_URL = "https://localhost:9004/"
CASES = (("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"), ("echo", {"value": "https"}, "echo=https"), ("add", {"a": 7, "b": 5}, "sum=12"))

async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        if not card.supported_interfaces or not all(i.url.startswith("https://") for i in card.supported_interfaces):
            raise AssertionError("Agent Card must advertise HTTPS interfaces only")
        extension_uri = card.capabilities.extensions[0].uri
        client = await agent.a2a_client(SERVER_URL)
        for skill_id, data, expected in CASES:
            actual = await _invoke(client, extension_uri, skill_id, data)
            if actual != expected:
                raise AssertionError(f"{skill_id}: {actual!r} != {expected!r}")
            print(f"PASS  HTTPS      {skill_id}")
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
