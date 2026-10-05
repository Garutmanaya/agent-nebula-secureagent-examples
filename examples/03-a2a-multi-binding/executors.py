"""Native a2a-sdk executors for this example."""
from __future__ import annotations

from typing import Any

from a2a.helpers import new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Role
from google.protobuf.json_format import MessageToDict


def _request_data(context: RequestContext) -> dict[str, Any]:
    if context.message is None:
        raise ValueError("skill requires an A2A user message")
    for part in context.message.parts:
        if part.HasField("data"):
            return MessageToDict(part.data)
    return {}


async def _reply(event_queue: EventQueue, text: str) -> None:
    await event_queue.enqueue_event(new_text_message(text, role=Role.ROLE_AGENT))


class HelloExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        await _reply(event_queue, "hello from SecureAgent")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("hello does not create a task")


class EchoExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        payload = _request_data(context)
        await _reply(event_queue, f"echo={payload.get('value', '')}")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("echo does not create a task")


class AddExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        payload = _request_data(context)
        await _reply(event_queue, f"sum={int(payload['a']) + int(payload['b'])}")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("add does not create a task")
