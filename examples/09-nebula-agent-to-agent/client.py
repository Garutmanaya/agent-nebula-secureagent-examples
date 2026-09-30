"""Agent-to-Agent example client.

This client demonstrates the external-client side of the Agent-to-Agent flow:

    Client
      -> Agent Nebula discovery
      -> Orchestrator Agent
      -> Agent Nebula discovery
      -> Provider Agent
      -> Orchestrator
      -> Client

The external client discovers and invokes only the orchestrator. The
orchestrator is responsible for discovering and invoking the downstream
provider.
"""

import asyncio
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

from examples.example_paths import config_path


HERE = Path(__file__).resolve().parent

ORCHESTRATOR_QUERY = "operations add"
ORCHESTRATOR_SKILL = "operations.add"


async def main() -> None:
    """Discover the orchestrator and invoke its operations.add skill."""

    # Create the SecureAgent client using the example's generated runtime
    # configuration. Agent Nebula configuration enables Registry discovery.
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        nebula_config=config_path(HERE, "nebula.conf"),
    )

    # Enable the official A2A protocol in client mode.
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(HERE, "a2aclient.conf"),
    )

    try:
        # Discover agents advertising the capability required by this client.
        # The external client expects the orchestrator to match this query.
        agents = await agent.discover(
            query=ORCHESTRATOR_QUERY,
        )

        # Print every discovery result so the example also demonstrates what
        # Agent Nebula discovery returned before selecting an agent.
        print(
            f"DISCOVERY: query={ORCHESTRATOR_QUERY!r} "
            f"returned {len(agents)} agent(s)"
        )

        for index, discovered_agent in enumerate(agents, start=1):
            print(
                f"  [{index}] "
                f"name={discovered_agent.display_name!r} "
                f"id={discovered_agent.agent_id!r}"
            )

        if not agents:
            raise AssertionError(
                "orchestrator not discovered for query "
                f"{ORCHESTRATOR_QUERY!r}"
            )

        orchestrator = agents[0]
        print(
            f"SELECTED: name={orchestrator.display_name!r} "
            f"id={orchestrator.agent_id!r} skill={ORCHESTRATOR_SKILL!r}"
        )
        print("FLOW: client -> orchestrator -> discovery -> provider -> orchestrator -> client")

        # Invoke the orchestrator. The orchestrator will independently discover
        # the downstream provider and forward the operations.add request.
        response = await agent.send_message(
            orchestrator,
            data={"a": 20, "b": 22},
            skill_id=ORCHESTRATOR_SKILL,
        )

        # Validate the final response returned through the complete
        # client -> orchestrator -> provider chain.
        text = response[0]["message"]["parts"][0]["text"]

        if text != "sum=42":
            raise AssertionError(f"unexpected result: {text!r}")

        print(
            "PASS  client -> orchestrator -> Registry discovery "
            "-> downstream provider"
        )
        print("RESULT: sum=42")

    finally:
        # SecureAgent owns asynchronous transports/resources and should always
        # be closed explicitly.
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
