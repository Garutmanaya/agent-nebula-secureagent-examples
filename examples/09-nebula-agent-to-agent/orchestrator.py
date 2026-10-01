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

# AGENT NEBULA CONFIGURATION:
# One SecureAgent composes official a2a-sdk server and client roles while
# adding Registry discovery and Nebula extension handling.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
)

# AGENT NEBULA CONFIGURATION: compose the official a2a-sdk server role.
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "orchestrator-server.conf"),
)

# AGENT NEBULA CONFIGURATION: compose the official a2a-sdk client role.
agent.use_protocol(
    "a2a",
    role="client",
    config=config_path(HERE, "a2aclient.conf"),
)


# AGENT NEBULA CONFIGURATION:
# @agent.skill adapts this handler to the official a2a-sdk AgentExecutor.
@agent.skill("operations.add")
async def orchestrated_add(payload):
    """Delegate an addition request to a dynamically discovered math agent."""
    print(f"ORCHESTRATOR: operations.add received data={dict(payload)!r}")

    # AGENT NEBULA EXTENSION:
    # Free-text Registry discovery searches indexed Agent Card metadata. The
    # orchestrator knows the required skill, not a provider address.
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

    # AGENT NEBULA EXTENSION:
    # skill_id selects the downstream skill through Nebula's A2A extension;
    # a2a-sdk owns the underlying A2A message execution.
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
