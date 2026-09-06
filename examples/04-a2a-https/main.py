"""HTTPS multi-skill A2A server."""
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

agent = SecureAgent(config=HERE / "secureagent.conf")
agent.use_protocol("a2a", role="server", config=HERE / "a2aserver.conf")


@agent.skill("hello")
async def hello(payload):
    """Return a deterministic greeting."""
    return {"message": "hello from SecureAgent"}


@agent.skill("echo")
async def echo(payload):
    """Echo the caller-provided value."""
    return {"message": f"echo={payload.get('value', '')}"}


@agent.skill("add")
async def add(payload):
    """Add two caller-provided integers."""
    return {"message": f"sum={int(payload['a']) + int(payload['b'])}"}


if __name__ == "__main__":
    agent.run()
