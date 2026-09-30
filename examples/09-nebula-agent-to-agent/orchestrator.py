"""Dual-role orchestrator for the Agent-to-Agent example.

The same SecureAgent instance serves ``operations.add`` to upstream callers and
acts as an A2A client for downstream providers. The downstream provider is
discovered from Agent Nebula at request time; no provider URL is hard-coded.
"""

from pathlib import Path

from agent_nebula_secureagent import SecureAgent

from examples.example_paths import config_path


HERE = Path(__file__).resolve().parent
DOWNSTREAM_QUERY = "math.add"
DOWNSTREAM_SKILL = "math.add"

agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
)

# Server role: expose the orchestrator to the external client.
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "orchestrator-server.conf"),
)

# Client role: discover and invoke the downstream provider.
agent.use_protocol(
    "a2a",
    role="client",
    config=config_path(HERE, "a2aclient.conf"),
)


@agent.skill("operations.add")
async def orchestrated_add(payload):
    """Delegate an addition request to a dynamically discovered math agent."""
    print(f"ORCHESTRATOR: operations.add received data={dict(payload)!r}")

    # Free-text discovery searches indexed Agent Card metadata. The orchestrator
    # intentionally knows the required skill, not a concrete provider address.
    providers = await agent.discover(query=DOWNSTREAM_QUERY)
    print(
        f"ORCHESTRATOR DISCOVERY: query={DOWNSTREAM_QUERY!r} "
        f"returned {len(providers)} agent(s)"
    )
    for index, provider in enumerate(providers, start=1):
        print(
            f"  [{index}] name={provider.display_name!r} "
            f"id={provider.agent_id!r}"
        )

    if not providers:
        return {"message": "no downstream math provider discovered"}

    provider = providers[0]
    print(
        f"ORCHESTRATOR SELECTED: name={provider.display_name!r} "
        f"id={provider.agent_id!r} skill={DOWNSTREAM_SKILL!r}"
    )

    responses = await agent.send_message(
        provider,
        data=payload,
        skill_id=DOWNSTREAM_SKILL,
    )

    message = responses[0].get("message", {})
    parts = message.get("parts", []) if isinstance(message, dict) else []
    text = parts[0].get("text") if parts and isinstance(parts[0], dict) else None

    print(f"ORCHESTRATOR RESULT: downstream response={text!r}")
    return {"message": text or "downstream response missing text"}


if __name__ == "__main__":
    print("START: operations orchestrator; skill='operations.add'")
    agent.run()
