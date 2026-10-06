"""Example 31: native A2A Task lifecycle with an A2UI artifact."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from pathlib import Path

from a2a.helpers import new_task_from_user_message, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

from a2ui_transport import a2ui_part
from presentation import load_presentation


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PRESENTATION = HERE / "presentation.json"


# -----------------------------------------------------------------------------
# Native A2A Task executor
# -----------------------------------------------------------------------------

class ReportExecutor(AgentExecutor):
    """Create a native Task whose application artifact contains A2UI."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("generate-report requires an A2A user message")

        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(
            TaskState.TASK_STATE_WORKING,
            new_text_message(
                "generating service report",
                context_id=task.context_id,
                task_id=task.id,
            ),
        )

        # Application business data is overlaid into an application-owned A2UI
        # JSON document. SecureAgent does not construct the presentation.
        document = load_presentation(
            PRESENTATION,
            {
                "rows": [
                    {"service": "Gateway", "region": "us-east", "status": "Healthy"},
                    {"service": "Registry", "region": "us-west", "status": "Healthy"},
                    {"service": "Policy", "region": "eu-west", "status": "Healthy"},
                ]
            },
        )

        # STANDARD A2A: the A2UI DataPart is carried by a native Task artifact.
        await updater.add_artifact(
            [a2ui_part([document])],
            artifact_id="service-report-a2ui",
            name="service-report",
        )

        await updater.complete(
            new_text_message(
                "service report complete",
                context_id=task.context_id,
                task_id=task.id,
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.task_id is None or context.context_id is None:
            raise ValueError("task cancellation requires task_id and context_id")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.update_status(TaskState.TASK_STATE_CANCELED)


# -----------------------------------------------------------------------------
# Agent configuration and skill registration
# -----------------------------------------------------------------------------

agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "a2aserver.conf"),
)
agent.a2a_skill("generate-report", ReportExecutor())


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("START: native A2A Task + A2UI artifact example server")
    agent.run()
