"""A2A multi-binding TLS."""
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

agent = SecureAgent(
    config=HERE / "secureagent.conf"
)
agent.use_protocol("a2a", role="server", config=HERE / "a2aserver.conf")


@agent.skill("hello")
def hello(payload):
    return {"message": "hello from SecureAgent"}


@agent.skill("echo")
def echo(payload):
    return {"message": f"echo={payload.get('value', '')}"}


@agent.skill("add")
def add(payload):
    return {"message": f"sum={int(payload.get('a', 0)) + int(payload.get('b', 0))}"}


if __name__ == "__main__":
    agent.run()
