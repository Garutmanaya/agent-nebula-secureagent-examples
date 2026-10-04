"""Example 24: mixed A2UI v1.0 Basic + Rich catalogs over native a2a-sdk."""
from pathlib import Path

from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
from a2ui_transport import a2ui_part
from presentation import WeatherDashboardPresenter

HERE = Path(__file__).resolve().parent
PRESENTER = WeatherDashboardPresenter(HERE / "presentation.json")


class WeatherDashboardExecutor(AgentExecutor):
    """Application executor that publishes a mixed-catalog A2UI surface."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        document = PRESENTER.create_surface(
            region="Northern Virginia",
            temperature=72,
            humidity=48,
            wind_speed=7,
            conditions="Clear",
        )
        await event_queue.enqueue_event(new_message([a2ui_part([document])]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("weather dashboard returns an immediate Message")


agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("weather-dashboard", WeatherDashboardExecutor())

if __name__ == "__main__":
    print("START: native A2A + direct A2UI mixed Basic/Rich server")
    agent.run()
