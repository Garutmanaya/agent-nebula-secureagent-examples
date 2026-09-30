"""Downstream math provider for the Agent-to-Agent orchestration example.

This process registers with Agent Nebula and exposes the ``math.add`` A2A skill.
The orchestrator discovers this provider dynamically; the external client never
invokes it directly.
"""

from pathlib import Path

from agent_nebula_secureagent import SecureAgent

from examples.example_paths import config_path


HERE = Path(__file__).resolve().parent

# This SecureAgent is an A2A server and an Agent Nebula registered provider.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
)
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "provider-server.conf"),
)


@agent.skill("math.add")
def add(payload):
    """Add two integers supplied by the upstream orchestrator."""
    a = int(payload.get("a", 0))
    b = int(payload.get("b", 0))
    result = a + b
    print(f"PROVIDER: math.add received a={a} b={b} -> sum={result}")
    return {"message": f"sum={result}"}


if __name__ == "__main__":
    print("START: downstream math provider; skill='math.add'")
    agent.run()
