"""A2UI Example 29 server."""

from pathlib import Path

from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

from a2ui_transport import a2ui_part
from presentation import load_presentation


# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent


# -----------------------------------------------------------------------------
# Native A2A skill
# -----------------------------------------------------------------------------

class ChartExecutor(AgentExecutor):
    """Return application-owned A2UI presentation JSON through native A2A."""

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        values = [("us-east", 80), ("us-west", 50), ("eu-west", 30)]
        series = [
            {"label": label, "value": value}
            for label, value in values
        ]
        presentation = load_presentation(
            HERE / "presentation.json",
            {"series": series},
        )
        await event_queue.enqueue_event(
            new_message([a2ui_part([presentation])])
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError


# -----------------------------------------------------------------------------
# SecureAgent composition
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
agent.a2a_skill("traffic-chart", ChartExecutor())


if __name__ == "__main__":
    agent.run()
