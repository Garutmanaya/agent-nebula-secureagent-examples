"""Example 23: direct A2UI v1.0 Basic Catalog over native a2a-sdk."""
from pathlib import Path

from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
from a2ui_transport import a2ui_part
from presentation import ForecastPresenter

HERE = Path(__file__).resolve().parent
PRESENTER = ForecastPresenter(HERE / "presentation.json")


class ForecastExecutor(AgentExecutor):
    """Application executor that emits A2UI directly through native a2a-sdk."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        document = PRESENTER.create_surface(
            region="Northern Virginia",
            temperature="72°F",
            conditions="Clear",
        )
        await event_queue.enqueue_event(new_message([a2ui_part([document])]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("forecast returns an immediate Message")


agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("forecast", ForecastExecutor())

if __name__ == "__main__":
    print("START: native A2A + direct A2UI Basic server")
    agent.run()
