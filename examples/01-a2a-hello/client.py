"""Basic A2A client using the native a2a-sdk client API."""

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
SERVER_URL = "http://localhost:9001/"


def _data_part(data: dict[str, object]) -> Part:
    """Build the official A2A v1.0 data part used by this example."""
    value = Value(struct_value=ParseDict(data, Struct()))
    return Part(data=value)


async def main() -> None:
    """Resolve the agent and invoke it through the official a2a-sdk Client."""
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(HERE, "a2aclient.conf"),
    )

    try:
        # AGENT NEBULA INTEGRATION:
        # SecureAgent applies configuration, transport and security policy, then
        # returns the official a2a.client.Client. Standard A2A operations below
        # are intentionally invoked directly on that SDK client.
        client = await agent.a2a_client(SERVER_URL)

        card = await agent.resolve_agent_card(SERVER_URL)
        print("Resolved Agent Card:", card.name or "<unnamed>")

        # STANDARD A2A: Message, Part, SendMessageRequest and send_message() are
        # all owned by a2a-sdk; SecureAgent does not define parallel wire models.
        request = SendMessageRequest(
            message=Message(
                role=Role.ROLE_USER,
                message_id=str(uuid.uuid4()),
                parts=[_data_part({"name": "Agent Nebula"})],
            )
        )
        async for response in client.send_message(request):
            if response.HasField("message"):
                print(get_message_text(response.message, delimiter=" "))
            else:
                print(response)
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
