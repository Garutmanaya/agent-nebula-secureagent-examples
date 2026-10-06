"""Example 21: native A2A push notifications."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import asyncio
from pathlib import Path
from a2a.helpers import new_task_from_user_message, new_text_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent

# -----------------------------------------------------------------------------
# Skill executors
# -----------------------------------------------------------------------------
class LongReportExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("long-report requires an A2A user message")
        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(TaskState.TASK_STATE_WORKING)
        await asyncio.sleep(0.75)
        await updater.add_artifact([new_text_part("push report ready")], name="push-report")
        await updater.complete(new_text_message("push report complete", context_id=task.context_id, task_id=task.id))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.task_id is None or context.context_id is None:
            raise ValueError("task cancellation requires task_id and context_id")
        await TaskUpdater(event_queue, context.task_id, context.context_id).update_status(TaskState.TASK_STATE_CANCELED)

# -----------------------------------------------------------------------------
# Agent configuration and skill registration
# -----------------------------------------------------------------------------
agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("long-report", LongReportExecutor())

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("START: SecureAgent native A2A push notification example server")
    agent.run()
