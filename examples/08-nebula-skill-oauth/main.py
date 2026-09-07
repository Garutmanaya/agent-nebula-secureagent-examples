"""Agent Nebula least-privilege skill OAuth."""
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

agent = SecureAgent(
    config=HERE / "secureagent.conf",
    nebula_config=HERE / "nebula.conf"
)
agent.use_protocol("a2a", role="server", config=HERE / "a2aserver.conf")


@agent.skill("hello", scopes=("hello.invoke",))
def hello(payload):
    return {"message": "hello from SecureAgent"}


@agent.skill("echo", scopes=("echo.invoke",))
def echo(payload):
    return {"message": f"echo={payload.get('value', '')}"}


@agent.skill("add", scopes=("add.invoke",))
def add(payload):
    return {"message": f"sum={int(payload.get('a', 0)) + int(payload.get('b', 0))}"}


if __name__ == "__main__":
    agent.run()
