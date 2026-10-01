"""Verify that selected AgentSkill IDs drive least-privilege OAuth scopes.

The client uses Agent Nebula free-text discovery to locate the provider, then
invokes each advertised business skill through the discovered provider object.
SecureAgent resolves the provider Agent Card and applies the configured OAuth
security requirements before sending the A2A request.
"""

import asyncio
from pathlib import Path

from agent_nebula_secureagent import SecureAgent

from examples.example_paths import config_path


HERE = Path(__file__).resolve().parent
PROVIDER_NAME = 'Skill OAuth Registry Agent'
DISCOVERY_QUERY = "hello"

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "registry"}, "echo=registry"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
)


def response_text(responses):
    """Extract the text value from a single A2A response message."""
    if len(responses) != 1:
        raise AssertionError(f"expected one response, got {len(responses)}")

    message = responses[0].get("message")
    if not isinstance(message, dict):
        raise AssertionError(f"missing A2A message: {responses[0]}")

    parts = message.get("parts")
    if not isinstance(parts, list) or not parts or not isinstance(parts[0], dict):
        raise AssertionError(f"missing A2A message parts: {message}")

    text = parts[0].get("text")
    if not isinstance(text, str):
        raise AssertionError(f"missing text response: {parts[0]}")

    return text


def print_discovery_results(found):
    """Display every Registry match before the example selects a provider."""
    print(f"DISCOVERY: query='hello' returned {len(found)} agent(s)")
    for index, discovered in enumerate(found, start=1):
        print(
            f"  [{index}] name={discovered.display_name!r} "
            f"id={discovered.agent_id!r}"
        )


async def main() -> None:
    """Discover the protected provider and verify all example skills."""
    # AGENT NEBULA CONFIGURATION / SECURITY:
    # SecureAgent configures Registry access and OAuth credential handling.
    # OAuth credentials are applied through the a2a-sdk client integration;
    # standard A2A request execution remains owned by a2a-sdk.
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        nebula_config=config_path(HERE, "nebula.conf"),
    )
    agent.use_protocol(
        "a2a",
        role="client",
        config=config_path(HERE, "a2aclient.conf"),
    )

    try:
        # AGENT NEBULA EXTENSION:
        # ``query`` maps to Registry free-text ``q`` and searches indexed Agent
        # Card metadata. Registry discovery is outside the A2A protocol.
        found = await agent.discover(query=DISCOVERY_QUERY)
        print_discovery_results(found)

        if not found:
            raise AssertionError(
                f"Registry returned no provider for query {DISCOVERY_QUERY!r}"
            )

        provider = next(
            (item for item in found if item.display_name == PROVIDER_NAME),
            found[0],
        )
        print(
            f"SELECTED: name={provider.display_name!r} "
            f"id={provider.agent_id!r}"
        )

        # AGENT NEBULA SECURITY / EXTENSION:
        # SecureAgent obtains/applies configured OAuth credentials and skill_id
        # activates Nebula skill selection. a2a-sdk owns the A2A operation.
        for skill_id, data, expected in SKILL_CASES:
            print(f"INVOKE: skill={skill_id!r} data={data!r}")
            actual = response_text(
                await agent.send_message(
                    provider,
                    data=data,
                    skill_id=skill_id,
                )
            )
            if actual != expected:
                raise AssertionError(
                    f"{skill_id}: expected {expected!r}, received {actual!r}"
                )
            print(f"PASS  least-privilege OAuth {skill_id} -> {actual}")

        print('RESULT: selected AgentSkill.id drove skill-specific OAuth authorization')
    finally:
        # Close transports and authentication resources owned by SecureAgent.
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
