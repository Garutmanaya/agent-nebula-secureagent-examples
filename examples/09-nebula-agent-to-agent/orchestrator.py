"""Dual-role A2A orchestrator that discovers its downstream provider."""
from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

from executors import OrchestratedAddExecutor

HERE = Path(__file__).resolve().parent

# The same SecureAgent owns a native A2A server role and configured A2A client
# role. Registry discovery supplies provider locations; it does not replace A2A.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
)
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "orchestrator-server.conf"),
)
agent.use_protocol(
    "a2a",
    role="client",
    config=config_path(HERE, "a2aclient.conf"),
)
agent.a2a_skill("operations.add", OrchestratedAddExecutor(agent))

if __name__ == "__main__":
    agent.run()
