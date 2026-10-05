"""External native A2A client for the Agent-to-Agent orchestration example."""
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
ORCHESTRATOR_QUERY = "operations add"
AGENT_CARD_PATH = "/.well-known/agent-card.json"


def _data_part(data: dict[str, object]) -> Part:
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


def _provider_base_url(agent_card_url: str) -> str:
    if not agent_card_url.endswith(AGENT_CARD_PATH):
        raise AssertionError(f"unexpected Agent Card URL: {agent_card_url}")
    return agent_card_url.removesuffix(AGENT_CARD_PATH)


async def main() -> None:
    """Discover and invoke the single-skill orchestrator through native A2A."""
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        nebula_config=config_path(HERE, "nebula.conf"),
    )
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))

    try:
        orchestrators = await agent.discover(query=ORCHESTRATOR_QUERY)
        if not orchestrators:
            raise AssertionError("operations orchestrator was not discovered")
        orchestrator = orchestrators[0]
        if not orchestrator.agent_card_url:
            raise AssertionError("orchestrator has no Agent Card URL")

        orchestrator_url = _provider_base_url(orchestrator.agent_card_url)
        card = await agent.resolve_agent_card(orchestrator_url)
        if {skill.id for skill in card.skills} != {"operations.add"}:
            raise AssertionError("unexpected orchestrator Agent Card skills")

        # The orchestrator has one skill, so no skill-selection extension is
        # required for the upstream call. Its executor performs downstream discovery.
        client = await agent.a2a_client(orchestrator_url)
        request = SendMessageRequest(
            message=Message(
                role=Role.ROLE_USER,
                message_id=str(uuid.uuid4()),
                parts=[_data_part({"a": 20, "b": 22})],
            )
        )
        responses = [response async for response in client.send_message(request)]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise AssertionError(f"unexpected orchestrator response: {responses}")
        actual = get_message_text(responses[0].message, delimiter=" ")
        if actual != "sum=42":
            raise AssertionError(f"unexpected result: {actual!r}")

        print("PASS  client -> orchestrator -> Registry -> provider -> orchestrator")
        print("RESULT: sum=42")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
