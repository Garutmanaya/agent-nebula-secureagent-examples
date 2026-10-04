"""Example 16: native a2a-sdk Message and Task execution through SecureAgent."""
from pathlib import Path

from a2a.helpers import new_task_from_user_message, new_text_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Role, TaskState

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent


class HelloExecutor(AgentExecutor):
    """STANDARD A2A: immediate execution returns one native Message event."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        await event_queue.enqueue_event(
            new_text_message("hello from native a2a-sdk", role=Role.ROLE_AGENT)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("hello does not create a task")


class ReportExecutor(AgentExecutor):
    """STANDARD A2A: application owns the complete native Task lifecycle."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("generate-reports requires an A2A user message")

        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(
            TaskState.TASK_STATE_WORKING,
            new_text_message(
                "generating reports",
                context_id=task.context_id,
                task_id=task.id,
            ),
        )

        for name, text in (
            ("daily-report", "daily report ready"),
            ("weekly-report", "weekly report ready"),
            ("monthly-report", "monthly report ready"),
        ):
            await updater.add_artifact([new_text_part(text)], name=name)

        await updater.complete(
            new_text_message(
                "all reports generated",
                context_id=task.context_id,
                task_id=task.id,
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.task_id is None or context.context_id is None:
            raise ValueError("task cancellation requires task_id and context_id")
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.update_status(TaskState.TASK_STATE_CANCELED)


# AGENT NEBULA CONFIGURATION: configuration, server composition, and lifecycle
# remain owned by SecureAgent/Platform; application execution remains native SDK.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
)
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))

# AGENT NEBULA EXTENSION: deterministic multi-skill dispatch selects one
# advertised skill; each selected implementation is a native AgentExecutor.
agent.a2a_skill("hello", HelloExecutor())
agent.a2a_skill("generate-reports", ReportExecutor())


if __name__ == "__main__":
    print("START: SecureAgent native A2A Task + HTTPS + OAuth example server")
    agent.run()
