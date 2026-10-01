"""Verify every skill exposed by the multi-skill A2A server."""
from __future__ import annotations

import asyncio
from pathlib import Path

from examples.example_paths import config_path

from a2a.types import AgentCard

from agent_nebula_secureagent import DiscoveredAgent, SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9002/"

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "multi-skill"}, "echo=multi-skill"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
)


def _direct_provider(agent_card: AgentCard, agent_card_url: str) -> DiscoveredAgent:
    """Adapt a direct SDK AgentCard for Nebula skill-selection convenience.

    AGENT NEBULA EXTENSION: A2A core does not define deterministic ``skill_id``
    dispatch. These multi-skill examples therefore use SecureAgent's formal
    skill-selection extension while retaining the official AgentCard model.
    """
    name = agent_card.name or agent_card_url
    return DiscoveredAgent(
        agent_id=name,
        display_name=name,
        agent_card_url=agent_card_url,
    )


def _response_text(responses: tuple[dict[str, object], ...]) -> str:
    """Extract the text returned by the example's stateless A2A skill."""
    if len(responses) != 1:
        raise AssertionError(f"expected one response, received {len(responses)}")
    message = responses[0].get("message")
    if not isinstance(message, dict):
        raise AssertionError(f"response does not contain an A2A message: {responses[0]}")
    parts = message.get("parts")
    if not isinstance(parts, list) or not parts or not isinstance(parts[0], dict):
        raise AssertionError(f"response does not contain message parts: {message}")
    text = parts[0].get("text")
    if not isinstance(text, str):
        raise AssertionError(f"response does not contain a text part: {parts[0]}")
    return text


async def _test_all_skills(agent: SecureAgent, provider: DiscoveredAgent, label: str) -> int:
    """Invoke and validate every skill advertised by this example."""
    passed = 0
    for skill_id, data, expected in SKILL_CASES:
        # AGENT NEBULA EXTENSION: skill_id selects one advertised skill through
        # the formal Nebula extension; A2A transport execution remains a2a-sdk.
        responses = await agent.send_message(
            provider,
            data=data,
            skill_id=skill_id,
        )
        actual = _response_text(responses)
        if actual != expected:
            raise AssertionError(
                f"{label}/{skill_id}: expected {expected!r}, received {actual!r}"
            )
        passed += 1
        print(f"PASS  {label:<10} {skill_id}")
    return passed


async def main() -> None:
    agent = SecureAgent(config=config_path(HERE, "secureagent.conf"))
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        advertised = {skill.id for skill in card.skills}
        expected = {case[0] for case in SKILL_CASES}
        if advertised != expected:
            raise AssertionError(f"unexpected advertised skills: {sorted(advertised)}")
        print(f"PASS  Agent Card skills: {', '.join(sorted(advertised))}")
        provider = _direct_provider(card, SERVER_URL)
        passed = await _test_all_skills(agent, provider, "JSON-RPC")
        print(f"RESULT: {passed}/{len(SKILL_CASES)} skill invocations passed")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
