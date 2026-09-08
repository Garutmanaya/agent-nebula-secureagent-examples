"""Agent Nebula OAuth protected A2A."""
from pathlib import Path

from examples.example_paths import config_path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf")
)
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))


@agent.skill("hello", scopes=("agent.invoke",))
def hello(payload):
    return {"message": "hello from SecureAgent"}


@agent.skill("echo", scopes=("agent.invoke",))
def echo(payload):
    return {"message": f"echo={payload.get('value', '')}"}


@agent.skill("add", scopes=("agent.invoke",))
def add(payload):
    return {"message": f"sum={int(payload.get('a', 0)) + int(payload.get('b', 0))}"}


if __name__ == "__main__":
    agent.run()
