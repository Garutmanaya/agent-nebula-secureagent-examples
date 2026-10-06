"""Example 25: selected native A2A skills return application-owned A2UI."""
from pathlib import Path

from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

from a2ui_transport import a2ui_part
from presentation import load_presentation

HERE = Path(__file__).resolve().parent
WEATHER_PRESENTATION = HERE / "presentations" / "weather.json"
SYSTEM_HEALTH_PRESENTATION = HERE / "presentations" / "system-health.json"


class WeatherExecutor(AgentExecutor):
    """Native A2A skill whose application result is an A2UI surface."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        document = load_presentation(
            WEATHER_PRESENTATION,
            {
                "region": "Northern Virginia",
                "temperature": "72°F",
                "conditions": "Clear",
            }
        )
        await event_queue.enqueue_event(new_message([a2ui_part([document])]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("weather returns an immediate Message")


class SystemHealthExecutor(AgentExecutor):
    """Independent native A2A skill with its own A2UI presentation."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        document = load_presentation(
            SYSTEM_HEALTH_PRESENTATION,
            {
                "service": "Agent Registry",
                "status": "Healthy",
                "latency": "18 ms",
            }
        )
        await event_queue.enqueue_event(new_message([a2ui_part([document])]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("system-health returns an immediate Message")


# SecureAgent owns configuration and the Agent Nebula multi-skill extension.
# Each selected implementation remains a native a2a-sdk AgentExecutor and
# creates its A2UI result directly; SecureAgent does not construct A2UI.
agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("weather", WeatherExecutor())
agent.a2a_skill("system-health", SystemHealthExecutor())


if __name__ == "__main__":
    print("START: native multi-skill A2A + direct A2UI skill results")
    agent.run()
