from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from pathlib import Path

from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from agent_nebula_secureagent import SecureAgent

from a2ui_transport import a2ui_part
from examples.example_paths import config_path
from presentation import load_presentation


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent


# -----------------------------------------------------------------------------
# Native A2A executor
# -----------------------------------------------------------------------------

class JsonSurfaceExecutor(AgentExecutor):
    """Return one application-owned A2UI presentation for an A2A skill."""

    def __init__(self, path: Path, data_model: dict):
        self.path = path
        self.data_model = data_model

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Load the presentation and emit it as an A2A DataPart."""

        presentation = load_presentation(
            self.path,
            self.data_model,
        )
        message = new_message(
            [a2ui_part([presentation])]
        )

        await event_queue.enqueue_event(message)

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not required by this deterministic example."""

        raise NotImplementedError


# -----------------------------------------------------------------------------
# SecureAgent configuration
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


# -----------------------------------------------------------------------------
# Skills
# -----------------------------------------------------------------------------

agent.a2a_skill(
    "inventory",
    JsonSurfaceExecutor(
        HERE / "inventory.json",
        {
            "rows": [
                {
                    "item": "Gateway",
                    "region": "us-east",
                    "available": "12",
                },
                {
                    "item": "Registry",
                    "region": "us-west",
                    "available": "7",
                },
                {
                    "item": "Policy",
                    "region": "eu-west",
                    "available": "4",
                },
            ]
        },
    ),
)

agent.a2a_skill(
    "traffic",
    JsonSurfaceExecutor(
        HERE / "traffic.json",
        {
            "series": [
                {"label": "us-east", "value": 80},
                {"label": "us-west", "value": 50},
                {"label": "eu-west", "value": 30},
            ]
        },
    ),
)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    agent.run()
