"""Agent Nebula least-privilege skill OAuth."""
from pathlib import Path

from examples.example_paths import config_path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

# AGENT NEBULA CONFIGURATION:
# SecureAgent creates the standard A2A agent from configuration and adds
# skill-scoped OAuth security. A2A protocol handling remains owned by a2a-sdk.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf")
)
# AGENT NEBULA CONFIGURATION:
# Compose the official a2a-sdk server stack from the protocol configuration.
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))


# AGENT NEBULA CONFIGURATION:
# @agent.skill is Nebula's config-driven skill registration API. Platform
# adapts these handlers to the official a2a-sdk AgentExecutor interface.
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
    print("START: SecureAgent A2A example server")
    agent.run()
