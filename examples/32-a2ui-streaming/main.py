"""Example 32: native A2A streaming carrying incremental A2UI updates."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import asyncio
from pathlib import Path

from a2a.helpers import new_task_from_user_message, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

from a2ui_transport import a2ui_part
from presentation import StreamingTrafficPresenter


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PRESENTER = StreamingTrafficPresenter(HERE / "presentation.json")
ARTIFACT_ID = "streaming-traffic-a2ui"

STREAM_SERIES = (
    [
        {"label": "us-east", "value": 20},
        {"label": "us-west", "value": 10},
        {"label": "eu-west", "value": 5},
    ],
    [
        {"label": "us-east", "value": 40},
        {"label": "us-west", "value": 25},
        {"label": "eu-west", "value": 15},
    ],
    [
        {"label": "us-east", "value": 60},
        {"label": "us-west", "value": 40},
        {"label": "eu-west", "value": 25},
    ],
    [
        {"label": "us-east", "value": 80},
        {"label": "us-west", "value": 50},
        {"label": "eu-west", "value": 30},
    ],
)


# -----------------------------------------------------------------------------
# Native A2A streaming executor
# -----------------------------------------------------------------------------

class StreamingTrafficExecutor(AgentExecutor):
    """Stream one A2UI surface followed by incremental data-model updates."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("stream-traffic requires an A2A user message")

        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(
            TaskState.TASK_STATE_WORKING,
            new_text_message(
                "streaming traffic presentation",
                context_id=task.context_id,
                task_id=task.id,
            ),
        )

        # STANDARD A2A STREAMING: every A2UI protocol message is emitted through
        # the native Task artifact stream. The application owns the A2UI JSON.
        for index, series in enumerate(STREAM_SERIES):
            if index == 0:
                document = PRESENTER.create_surface(series)
            else:
                document = PRESENTER.update_series(series)

            await updater.add_artifact(
                [a2ui_part([document])],
                artifact_id=ARTIFACT_ID,
                name="streaming-traffic",
                append=index > 0,
                last_chunk=index == len(STREAM_SERIES) - 1,
            )
            await asyncio.sleep(1.0)

        await updater.complete(
            new_text_message(
                "traffic presentation stream complete",
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
agent.a2a_skill("stream-traffic", StreamingTrafficExecutor())


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("START: native A2A streaming + incremental A2UI example server")
    agent.run()
