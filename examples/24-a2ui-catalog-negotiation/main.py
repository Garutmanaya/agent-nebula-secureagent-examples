"""Example 24: A2UI v1.0 catalog negotiation over native a2a-sdk."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from pathlib import Path

from a2a.helpers import new_data_part, new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from google.protobuf.json_format import MessageToDict

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
from presentation import load_presentation

# -----------------------------------------------------------------------------
# Example configuration
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"
PRESENTATION = HERE / "presentation.json"

# -----------------------------------------------------------------------------
# Skill executors
# -----------------------------------------------------------------------------
class DashboardExecutor(AgentExecutor):
    """Select an A2UI catalog from renderer capabilities on this turn."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("dashboard requires an A2A user message")
        metadata = context.metadata
        renderer = metadata.get("a2uiRendererCapabilities", {}).get("v1.0", {})
        supported = list(renderer.get("supportedCatalogIds", []))
        #metadata = MessageToDict(context.message.metadata) if context.message.HasField("metadata") else {}
        #renderer = metadata.get("a2uiRendererCapabilities", {}).get("v1.0", {})
        #supported = list(renderer.get("supportedCatalogIds", []))
        document = load_presentation(PRESENTATION, supported)
        part = new_data_part({"messages": [document]}, media_type=A2UI_MIME_TYPE)
        await event_queue.enqueue_event(new_message([part]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("dashboard returns an immediate Message")

# -----------------------------------------------------------------------------
# Agent configuration and skill registration
# -----------------------------------------------------------------------------
agent = SecureAgent(config=config_path(HERE, "secureagent.conf"), a2ui_config=config_path(HERE, "a2ui.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("dashboard", DashboardExecutor())

# -----------------------------------------------------------------------------
# Application entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("START: native A2A + A2UI v1.0 catalog negotiation server")
    agent.run()
