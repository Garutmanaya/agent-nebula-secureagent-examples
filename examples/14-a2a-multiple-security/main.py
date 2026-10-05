"""Example 14: A2A security acceptance server using a native a2a-sdk executor."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from pathlib import Path

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent
from executors import HelloExecutor

# -----------------------------------------------------------------------------
# Agent configuration and skill registration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent

# Agent Card security metadata is authoritative. Private verifier/trust material
# stays in a2aserver.conf; Platform enforces it before application execution.
agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("hello", HelloExecutor())

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    agent.run()
