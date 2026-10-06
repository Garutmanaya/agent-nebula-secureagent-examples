"""Example 18: native a2a-sdk streaming execution."""
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
class StreamingExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("stream-report requires an A2A user message")
        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(
            TaskState.TASK_STATE_WORKING,
            new_text_message(
                "stream started",
                context_id=task.context_id,
                task_id=task.id,
            ),
        )
        for index, text in enumerate(("chunk one", "chunk two", "chunk three"), start=1):
            await updater.add_artifact(
                [new_text_part(text)],
                artifact_id="streamed-report",
                name="streamed-report",
                append=index > 1,
                last_chunk=index == 3,
            )
            await asyncio.sleep(0.05)
        await updater.complete(new_text_message("stream complete", context_id=task.context_id, task_id=task.id))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.task_id is None or context.context_id is None:
            raise ValueError("task cancellation requires task_id and context_id")
        await TaskUpdater(
            event_queue,
            context.task_id,
            context.context_id,
        ).update_status(TaskState.TASK_STATE_CANCELED)

# -----------------------------------------------------------------------------
# Agent configuration and skill registration
# -----------------------------------------------------------------------------
agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("stream-report", StreamingExecutor())

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("START: SecureAgent native A2A streaming example server")
    agent.run()
