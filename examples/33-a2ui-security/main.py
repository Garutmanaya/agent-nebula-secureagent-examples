"""Example 33: existing Nebula HTTPS/OAuth security protecting A2UI over A2A."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

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
PRESENTATION_PATH = HERE / "presentation.json"


# -----------------------------------------------------------------------------
# Native A2A executor
# -----------------------------------------------------------------------------

class ChartExecutor(AgentExecutor):
    """Return an A2UI BarChart through a normal native A2A Message."""

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        series = [
            {"label": "us-east", "value": 80},
            {"label": "us-west", "value": 50},
            {"label": "eu-west", "value": 30},
        ]
        presentation = load_presentation(
            PRESENTATION_PATH,
            {"series": series},
        )
        response = new_message([a2ui_part([presentation])])
        await event_queue.enqueue_event(response)

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        raise NotImplementedError


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
agent.a2a_skill("traffic-chart", ChartExecutor())


# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("START: HTTPS + OAuth protected A2UI over native A2A")
    agent.run()
