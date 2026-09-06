"""Verify all example skills independently through every A2A protocol binding."""
from __future__ import annotations

import asyncio
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9003/"
BINDINGS = (
    ("JSON-RPC", "a2aclient-jsonrpc.conf", "JSONRPC"),
    ("HTTP+JSON", "a2aclient-http-json.conf", "HTTP+JSON"),
    ("gRPC", "a2aclient-grpc.conf", "GRPC"),
)

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "multi-skill"}, "echo=multi-skill"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
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


async def _test_all_skills(agent: SecureAgent, server_url: str, label: str) -> int:
    """Invoke and validate every skill advertised by this example."""
    passed = 0
    for skill_id, data, expected in SKILL_CASES:
        responses = await agent.send_message_to(
            server_url,
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


async def _test_binding(label: str, config_name: str) -> int:
    # A separate client instance forces the official A2A client to negotiate only
    # the binding under test instead of falling back to another advertised interface.
    agent = SecureAgent(config=HERE / "secureagent.conf")
    agent.use_protocol("a2a", role="client", config=HERE / config_name)
    try:
        return await _test_all_skills(agent, SERVER_URL, label)
    finally:
        await agent.close()


async def main() -> None:
    discovery = SecureAgent(config=HERE / "secureagent.conf")
    discovery.use_protocol("a2a", role="client", config=HERE / "a2aclient-jsonrpc.conf")
    try:
        card = await discovery.resolve_agent_card(SERVER_URL)
    finally:
        await discovery.close()

    advertised_skills = {skill["id"] for skill in card.get("skills", [])}
    expected_skills = {case[0] for case in SKILL_CASES}
    if advertised_skills != expected_skills:
        raise AssertionError(f"unexpected advertised skills: {sorted(advertised_skills)}")

    advertised_bindings = {
        interface["protocolBinding"] for interface in card.get("supportedInterfaces", [])
    }
    expected_bindings = {item[2] for item in BINDINGS}
    if advertised_bindings != expected_bindings:
        raise AssertionError(f"unexpected bindings: {sorted(advertised_bindings)}")
    print(f"PASS  Agent Card bindings: {', '.join(sorted(advertised_bindings))}")

    passed = 0
    for label, config_name, _ in BINDINGS:
        print(f"Testing {label}")
        passed += await _test_binding(label, config_name)

    total = len(BINDINGS) * len(SKILL_CASES)
    print(f"RESULT: {passed}/{total} binding/skill invocations passed")


if __name__ == "__main__":
    asyncio.run(main())
