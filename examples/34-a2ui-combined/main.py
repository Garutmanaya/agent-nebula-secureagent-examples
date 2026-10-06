"""Example 34: security + multi-skill + native Task/streaming + A2UI."""

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
STREAM_INTERVAL_SECONDS = 1.0
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
# Native Task skill
# -----------------------------------------------------------------------------

class ServiceReportExecutor(AgentExecutor):
    """Create a native Task whose artifact carries an A2UI report surface."""

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        if context.message is None:
            raise ValueError("service-report requires an A2A user message")

        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(TaskState.TASK_STATE_WORKING)

        series = [
            {"label": "healthy", "value": 3},
            {"label": "warning", "value": 1},
            {"label": "critical", "value": 0},
        ]
        await updater.add_artifact(
            [a2ui_part([PRESENTER.create_surface(series)])],
            name="service-report-a2ui",
        )
        await updater.complete(
            new_text_message(
                "service report complete",
                context_id=task.context_id,
                task_id=task.id,
            )
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        if context.task_id is None or context.context_id is None:
            raise ValueError("task cancellation requires task_id and context_id")

        updater = TaskUpdater(
            event_queue,
            context.task_id,
            context.context_id,
        )
        await updater.update_status(TaskState.TASK_STATE_CANCELED)


# -----------------------------------------------------------------------------
# Native streaming skill
# -----------------------------------------------------------------------------

class StreamingTrafficExecutor(AgentExecutor):
    """Stream incremental A2UI updates through a native A2A Task artifact."""

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        if context.message is None:
            raise ValueError("stream-traffic requires an A2A user message")

        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(TaskState.TASK_STATE_WORKING)

        for index, series in enumerate(STREAM_SERIES):
            document = (
                PRESENTER.create_surface(series)
                if index == 0
                else PRESENTER.update_series(series)
            )
            await updater.add_artifact(
                [a2ui_part([document])],
                artifact_id="combined-traffic-a2ui",
                name="combined-traffic",
                append=index > 0,
                last_chunk=index == len(STREAM_SERIES) - 1,
            )
            await asyncio.sleep(STREAM_INTERVAL_SECONDS)

        await updater.complete(
            new_text_message(
                "traffic stream complete",
                context_id=task.context_id,
                task_id=task.id,
            )
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        if context.task_id is None or context.context_id is None:
            raise ValueError("task cancellation requires task_id and context_id")

        updater = TaskUpdater(
            event_queue,
            context.task_id,
            context.context_id,
        )
        await updater.update_status(TaskState.TASK_STATE_CANCELED)


# -----------------------------------------------------------------------------
# SecureAgent configuration
# -----------------------------------------------------------------------------

agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    nebula_config=config_path(HERE, "nebula.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "a2aserver.conf"),
)
agent.a2a_skill("service-report", ServiceReportExecutor())
agent.a2a_skill("stream-traffic", StreamingTrafficExecutor())


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("START: HTTPS + OAuth + multi-skill + Task/streaming + A2UI server")
    agent.run()
