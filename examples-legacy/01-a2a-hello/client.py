"""Basic A2A client for the local SecureAgent hello server."""

from __future__ import annotations

import asyncio
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9001/"


async def main() -> None:
    """Invoke the server's advertised ``hello`` skill through SecureAgent."""
    agent = SecureAgent(config=HERE / "secureagent.conf")
    agent.use_protocol(
        "a2a",
        role="client",
        config=HERE / "a2aclient.conf",
    )

    agent_card = await agent.resolve_agent_card(SERVER_URL)
    print(
        "Resolved Agent Card:",
        agent_card.get("name", "<unnamed>"),
    )

    responses = await agent.send_message_to(
        SERVER_URL,
        data={"name": "Agent Nebula"},
        skill_id="hello",
    )
    for response in responses:
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
