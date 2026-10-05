"""Registry-discovered downstream math provider."""
from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

from executors import MathAddExecutor

HERE = Path(__file__).resolve().parent

agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
)
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "provider-server.conf"),
)
agent.a2a_skill("math.add", MathAddExecutor())

if __name__ == "__main__":
    agent.run()
