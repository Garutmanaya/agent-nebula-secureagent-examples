"""04-a2a-https A2A server."""
from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

from executors import AddExecutor, EchoExecutor, HelloExecutor

HERE = Path(__file__).resolve().parent

agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("hello", HelloExecutor())
agent.a2a_skill("echo", EchoExecutor())
agent.a2a_skill("add", AddExecutor())

if __name__ == "__main__":
    agent.run()
