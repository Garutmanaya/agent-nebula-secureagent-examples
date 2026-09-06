"""Structured input."""
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

agent = SecureAgent(config=HERE / "secureagent.conf")
agent.use_protocol("a2a", role="server", config=HERE / "a2aserver.conf")


@agent.skill("example.invoke")
def handle(payload):
    """Execute the example business capability."""
    name = str(payload.get("name", "")).strip()
    if not name:
        raise ValueError("name is required")
    return {"greeting": f"Hello, {name}"}


if __name__ == "__main__":
    agent.run()
