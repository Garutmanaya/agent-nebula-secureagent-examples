"""Verify API-key authentication through the native a2a-sdk client."""
from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

from a2a.helpers import get_message_text
from a2a.types import Message, Part, Role, SendMessageRequest
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct, Value

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "https://localhost:9010/"


def _data_part(data: dict[str, object]) -> Part:
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))

    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        if {skill.id for skill in card.skills} != {"hello"}:
            raise AssertionError("API-key Agent Card must advertise only the hello skill")

        # Platform applies the Agent Card's API-key requirement through the
        # official a2a-sdk ClientCallInterceptor boundary.
        client = await agent.a2a_client(SERVER_URL)
        request = SendMessageRequest(
            message=Message(
                role=Role.ROLE_USER,
                message_id=str(uuid.uuid4()),
                parts=[_data_part({"name": "Agent Nebula"})],
            )
        )
        responses = [event async for event in client.send_message(request)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"expected one Message response: {responses}")
        actual = get_message_text(responses[0].message, delimiter=" ")
        if actual != "authenticated hello":
            raise AssertionError(f"unexpected response: {actual!r}")
        print("PASS  API-key authenticated A2A invocation")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
