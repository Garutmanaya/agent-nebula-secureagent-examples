"""Native a2a-sdk executors for the Agent-to-Agent orchestration example."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import annotations

import uuid
from typing import Any

from a2a.client import ClientCallContext
from a2a.client.service_parameters import ServiceParametersFactory, with_a2a_extensions
from a2a.helpers import get_message_text, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Message, Part, Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.struct_pb2 import Struct, Value

AGENT_CARD_PATH = "/.well-known/agent-card.json"
DOWNSTREAM_QUERY = "math.add"
DOWNSTREAM_SKILL = "math.add"


# -----------------------------------------------------------------------------
# A2A request helpers
# -----------------------------------------------------------------------------

def _request_data(context: RequestContext) -> dict[str, Any]:
    """Return the first standard A2A data part from an incoming request."""
    if context.message is None:
        raise ValueError("skill requires an A2A user message")
    for part in context.message.parts:
        if part.HasField("data"):
            return MessageToDict(part.data)
    return {}


def _data_part(data: dict[str, Any]) -> Part:
    return Part(data=Value(struct_value=ParseDict(data, Struct())))


def _provider_base_url(agent_card_url: str) -> str:
    if not agent_card_url.endswith(AGENT_CARD_PATH):
        raise ValueError(f"unexpected Agent Card URL: {agent_card_url}")
    return agent_card_url.removesuffix(AGENT_CARD_PATH)


def _skill_request(extension_uri: str, skill_id: str, data: dict[str, Any]):
    """Build the standard A2A request plus Nebula skill-selection extension context."""
    return (
        SendMessageRequest(
            message=Message(
                role=Role.ROLE_USER,
                message_id=str(uuid.uuid4()),
                parts=[_data_part(data)],
            ),
            metadata=ParseDict({extension_uri: {"skillId": skill_id}}, Struct()),
        ),
        ClientCallContext(
            state={"agent_nebula.a2a.skill_id": skill_id},
            service_parameters=ServiceParametersFactory.create(
                [with_a2a_extensions([extension_uri])]
            ),
        ),
    )


# -----------------------------------------------------------------------------
# Skill executors
# -----------------------------------------------------------------------------

class MathAddExecutor(AgentExecutor):
    """Provide the downstream deterministic math.add skill."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        payload = _request_data(context)
        result = int(payload["a"]) + int(payload["b"])
        await event_queue.enqueue_event(
            new_text_message(f"sum={result}", role=Role.ROLE_AGENT)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("math.add does not create a task")


class OrchestratedAddExecutor(AgentExecutor):
    """Discover a math provider and delegate the request through native A2A."""

    def __init__(self, agent) -> None:
        self._agent = agent

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        payload = _request_data(context)

        # Registry discovery is Agent Nebula functionality. The downstream A2A
        # exchange itself uses the authoritative Agent Card and native SDK client.
        providers = await self._agent.discover(query=DOWNSTREAM_QUERY)
        if not providers:
            raise RuntimeError("no downstream math provider discovered")
        provider = providers[0]
        if not provider.agent_card_url:
            raise RuntimeError("downstream provider has no Agent Card URL")

        provider_url = _provider_base_url(provider.agent_card_url)
        card = await self._agent.resolve_agent_card(provider_url)
        if DOWNSTREAM_SKILL not in {skill.id for skill in card.skills}:
            raise RuntimeError("downstream provider does not advertise math.add")
        extensions = tuple(card.capabilities.extensions)
        if len(extensions) != 1:
            raise RuntimeError("downstream provider must advertise skill selection")

        client = await self._agent.a2a_client(provider_url)
        request, call_context = _skill_request(
            extensions[0].uri,
            DOWNSTREAM_SKILL,
            payload,
        )
        responses = [
            response
            async for response in client.send_message(request, context=call_context)
        ]
        if len(responses) != 1 or not responses[0].HasField("message"):
            raise RuntimeError(f"unexpected downstream response: {responses}")

        result = get_message_text(responses[0].message, delimiter=" ")
        await event_queue.enqueue_event(new_text_message(result, role=Role.ROLE_AGENT))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("operations.add does not create a task")
