"""Basic A2A server."""
from pathlib import Path

from examples.example_paths import config_path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent

# AGENT NEBULA CONFIGURATION:
# SecureAgent creates the agent from configuration and adapts the configured
# skills to the official a2a-sdk server interfaces. A2A protocol handling
# remains owned by a2a-sdk.
agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
# AGENT NEBULA CONFIGURATION:
# Enable and configure the A2A server role. Platform composes the official
# a2a-sdk server, request handler, transports, and AgentExecutor adapter.
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "a2aserver.conf"),
)


# AGENT NEBULA CONFIGURATION:
# @agent.skill is the configuration-friendly registration API. Platform
# adapts this handler to the official a2a-sdk AgentExecutor contract.
@agent.skill("hello")
async def hello(payload):
    """Execute the example business capability."""
    return {"message": "hello from SecureAgent", "payload": dict(payload)}


if __name__ == "__main__":
    print("START: SecureAgent A2A example server")
    agent.run()
