"""Example 26: browser A2UI action -> native A2A -> application A2UI update."""
from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
from a2ui_transport import a2ui_messages, a2ui_part
from presentation import CounterPresenter, SURFACE_ID
HERE = Path(__file__).resolve().parent
PRESENTER = CounterPresenter(HERE / "presentation.json")

class CounterExecutor(AgentExecutor):
    """Native A2A executor that handles initial UI and renderer A2UI actions."""
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        action = self._action(context)
        document = PRESENTER.create_surface(0) if action is None else PRESENTER.update_count(self._updated_count(context, action))
        await event_queue.enqueue_event(new_message([a2ui_part([document])]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("counter returns immediate A2A Messages")

    @staticmethod
    def _action(context: RequestContext) -> Mapping[str, Any] | None:
        if context.message is None:
            return None
        for document in a2ui_messages(context.message):
            action = document.get("action")
            if not isinstance(action, Mapping):
                continue
            if action.get("surfaceId") != SURFACE_ID:
                raise ValueError(f"unexpected surface: {action.get('surfaceId')}")
            if action.get("name") != "counter.increment":
                raise ValueError(f"unexpected action: {action.get('name')}")
            return action
        return None

    @staticmethod
    def _updated_count(context: RequestContext, action: Mapping[str, Any]) -> int:
        current = 0
        if context.message is not None:
            client_model = context.metadata.get("a2uiClientDataModel", {})
            current = int(client_model.get("surfaces", {}).get(SURFACE_ID, {}).get("count", 0))
        action_context = action.get("context", {})
        delta = action_context.get("delta", 1) if isinstance(action_context, Mapping) else 1
        return current + int(delta)

agent = SecureAgent(config=config_path(HERE, "secureagent.conf"), a2ui_config=config_path(HERE, "a2ui.conf"))
agent.use_protocol("a2a", role="server", config=config_path(HERE, "a2aserver.conf"))
agent.a2a_skill("counter", CounterExecutor())

if __name__ == "__main__":
    print("START: native A2A + direct bidirectional A2UI actions")
    agent.run()
