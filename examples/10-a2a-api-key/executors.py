"""Native a2a-sdk executor for Example 10."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from a2a.helpers import new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Role


# -----------------------------------------------------------------------------
# Skill executors
# -----------------------------------------------------------------------------

class HelloExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        await event_queue.enqueue_event(
            new_text_message("authenticated hello", role=Role.ROLE_AGENT)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("hello does not create a task")
