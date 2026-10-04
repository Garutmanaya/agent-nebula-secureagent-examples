"""Example 27: browser A2UI form -> native A2A -> application result update."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from google.protobuf.json_format import MessageToDict

from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path

from a2ui_transport import a2ui_messages, a2ui_part
from presentation import ContactFormPresenter, SURFACE_ID

HERE = Path(__file__).resolve().parent
PRESENTER = ContactFormPresenter(HERE / "presentation.json")


class ContactFormExecutor(AgentExecutor):
    """Handle initial form creation and submitted A2UI form actions."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        action = self._action(context)
        if action is None:
            document = PRESENTER.create_surface()
        else:
            form = self._submitted_form(context, action)
            document = PRESENTER.update_result(self._submission_result(form))

        await event_queue.enqueue_event(new_message([a2ui_part([document])]))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("contact form returns immediate A2A Messages")

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
            if action.get("name") != "contact.submit":
                raise ValueError(f"unexpected action: {action.get('name')}")
            return action

        return None

    @staticmethod
    def _submitted_form(
        context: RequestContext,
        action: Mapping[str, Any],
    ) -> dict[str, str]:
        """Read synchronized browser state and verify resolved action context."""
        if context.message is None:
            raise ValueError("form action requires an A2A message")

        payload = MessageToDict(context.message, preserving_proto_field_name=True)
        client_model = payload.get("metadata", {}).get("a2uiClientDataModel", {})
        surface_model = client_model.get("surfaces", {}).get(SURFACE_ID, {})
        name = str(surface_model.get("name", "")).strip()
        email = str(surface_model.get("email", "")).strip()

        action_context = action.get("context", {})
        if isinstance(action_context, Mapping):
            resolved_name = str(action_context.get("name", "")).strip()
            resolved_email = str(action_context.get("email", "")).strip()
            if resolved_name and resolved_name != name:
                raise ValueError("action name does not match synchronized data model")
            if resolved_email and resolved_email != email:
                raise ValueError("action email does not match synchronized data model")

        return {"name": name, "email": email}

    @staticmethod
    def _submission_result(form: Mapping[str, str]) -> str:
        """Perform application validation and return user-visible state."""
        if not form["name"]:
            return "Name is required."
        if not form["email"] or "@" not in form["email"]:
            return "A valid email address is required."
        return f"Submitted: {form['name']} <{form['email']}>"


agent = SecureAgent(
    config=config_path(HERE, "secureagent.conf"),
    a2ui_config=config_path(HERE, "a2ui.conf"),
)
agent.use_protocol(
    "a2a",
    role="server",
    config=config_path(HERE, "a2aserver.conf"),
)
agent.a2a_skill("contact-form", ContactFormExecutor())


if __name__ == "__main__":
    print("START: native A2A + direct A2UI form submission")
    agent.run()
