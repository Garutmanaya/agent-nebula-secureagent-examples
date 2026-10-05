"""Example 20: authenticated native A2A Extended Agent Card."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from pathlib import Path
from a2a.helpers import new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Role
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent

# -----------------------------------------------------------------------------
# Skill executors
# -----------------------------------------------------------------------------
class HelloExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        await event_queue.enqueue_event(new_text_message("hello from extended-card agent", role=Role.ROLE_AGENT))
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("hello does not create a task")

# -----------------------------------------------------------------------------
# Agent configuration and skill registration
# -----------------------------------------------------------------------------
agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("hello", HelloExecutor())

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("START: SecureAgent native A2A extended Agent Card example server")
    agent.run()
