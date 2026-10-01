"""Discover an A2A provider through Agent Nebula and invoke its advertised skills."""

import asyncio
from pathlib import Path

from examples.example_paths import config_path

from agent_nebula_secureagent import SecureAgent


HERE = Path(__file__).resolve().parent

PROVIDER_NAME = "Registry Discovery Agent"

SKILL_CASES = (
    ("hello", {"name": "Agent Nebula"}, "hello from SecureAgent"),
    ("echo", {"value": "registry"}, "echo=registry"),
    ("add", {"a": 7, "b": 5}, "sum=12"),
)


def response_text(responses):
    """Extract the text payload from a single A2A response message."""
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
    """Print the Agent Nebula Registry discovery results."""
    print(f"\nRegistry discovery returned {len(found)} agent(s):")

    for index, discovered in enumerate(found, start=1):
        print(f"\n  [{index}] {discovered.display_name}")
        print(f"      agent_id       : {discovered.agent_id}")
        print(f"      agent_card_url : {discovered.agent_card_url}")
        print(f"      protocols      : {discovered.protocols}")
        print(f"      skills         : {discovered.skills}")


async def main():
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
        # Registry discovery is Agent Nebula functionality; it is not part of
        # the A2A protocol or a2a-sdk. Discovery returns a Nebula provider
        # reference containing the registered Agent Card location.
        found = await agent.discover(query="hello")

        if not found:
            raise AssertionError(
                "Agent Nebula Registry returned no provider "
                "for query 'hello'"
            )

        print_discovery_results(found)

        provider = next(
            (
                item
                for item in found
                if item.display_name == PROVIDER_NAME
            ),
            found[0],
        )

        print("\nSELECTED AGENT:")
        print(f"  name           : {provider.display_name}")
        print(f"  agent_id       : {provider.agent_id}")
        print(f"  agent_card_url : {provider.agent_card_url}")
        print(f"\nPASS  Registry discovery: {provider.display_name}")

        if not provider.agent_card_url:
            raise AssertionError(
                "Registry discovery result does not contain an Agent Card URL"
            )

        # STANDARD A2A / AGENT NEBULA INTEGRATION:
        # resolve_agent_card() exposes the official a2a-sdk AgentCard model.
        # Registry stores the complete well-known Agent Card URL, while the
        # SDK resolver is initialized with the provider base URL.
        agent_card_path = "/.well-known/agent-card.json"

        if not provider.agent_card_url.endswith(agent_card_path):
            raise AssertionError(
                f"unexpected Agent Card URL: {provider.agent_card_url}"
            )

        provider_base_url = provider.agent_card_url.removesuffix(agent_card_path)
        agent_card = await agent.resolve_agent_card(provider_base_url)

        print("\nResolved A2A Agent Card:")
        print(f"  name       : {agent_card.name}")
        print(f"  skills     : {[skill.id for skill in agent_card.skills]}")
        print(f"  interfaces : {list(agent_card.supported_interfaces)}")

        advertised_skills = {skill.id for skill in agent_card.skills}

        # AGENT NEBULA EXTENSION:
        # send_message(provider, skill_id=...) is a Nebula convenience API for
        # Registry-discovered providers. skill_id is carried by the Nebula
        # skill-selection A2A extension; a2a-sdk still owns A2A execution.
        for skill_id, data, expected in SKILL_CASES:
            if skill_id not in advertised_skills:
                raise AssertionError(
                    f"Agent Card does not advertise skill {skill_id!r}"
                )

            actual = response_text(
                await agent.send_message(
                    provider,
                    data=data,
                    skill_id=skill_id,
                )
            )

            if actual != expected:
                raise AssertionError(
                    f"{skill_id}: {actual!r} != {expected!r}"
                )

            print(f"PASS  discovered provider {skill_id}")

        print(
            "\nRESULT: registration, Registry discovery, Agent Card "
            "resolution, and all skill invocations passed"
        )

    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
