"""Verify A2A skill selection and A2UI v1.0 output end to end."""
from __future__ import annotations

import asyncio
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from examples.example_paths import config_path

from agent_nebula_secureagent import DiscoveredAgent, SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9011/"
A2UI_EXTENSION_URI = "https://a2ui.org/a2a-extension/a2ui/v1.0"
A2UI_MIME_TYPE = "application/a2ui+json"



def _direct_provider(agent_card: dict, agent_card_url: str) -> DiscoveredAgent:
    """Adapt direct Agent Card discovery to the current SecureAgent invocation API."""
    return DiscoveredAgent(
        agent_id=str(agent_card.get("name") or agent_card_url),
        display_name=str(agent_card.get("name") or agent_card_url),
        agent_card_url=agent_card_url,
    )

def _find_parts(value: Any) -> list[Mapping[str, Any]]:
    """Return normalized A2A parts without depending on A2A SDK wire models."""
    result: list[Mapping[str, Any]] = []
    if isinstance(value, Mapping):
        parts = value.get("parts")
        if isinstance(parts, list):
            result.extend(part for part in parts if isinstance(part, Mapping))
        for child in value.values():
            result.extend(_find_parts(child))
    elif isinstance(value, list | tuple):
        for child in value:
            result.extend(_find_parts(child))
    return result


def _assert_agent_card(card: Mapping[str, Any]) -> None:
    skills = {skill["id"] for skill in card.get("skills", [])}
    if skills != {"summary", "forecast"}:
        raise AssertionError(f"unexpected Agent Card skills: {sorted(skills)}")

    capabilities = card.get("capabilities", {})
    extensions = capabilities.get("extensions", []) if isinstance(capabilities, Mapping) else []
    uris = {
        extension.get("uri")
        for extension in extensions
        if isinstance(extension, Mapping)
    }
    if A2UI_EXTENSION_URI not in uris:
        raise AssertionError(f"Agent Card does not advertise {A2UI_EXTENSION_URI}")
    print("PASS  Agent Card advertises forecast + summary and A2UI v1.0")


def _assert_forecast(responses: tuple[dict[str, object], ...]) -> None:
    parts = _find_parts(responses)
    business = next(
        (
            part.get("data")
            for part in parts
            if isinstance(part.get("data"), Mapping)
            and part.get("metadata", {}).get("mimeType") != A2UI_MIME_TYPE
        ),
        None,
    )
    if not isinstance(business, Mapping) or business.get("units") != 1250:
        raise AssertionError(f"structured forecast data missing: {responses}")

    a2ui = next(
        (
            part
            for part in parts
            if isinstance(part.get("metadata"), Mapping)
            and part["metadata"].get("mimeType") == A2UI_MIME_TYPE
        ),
        None,
    )
    if a2ui is None:
        raise AssertionError("A2UI DataPart was not returned")
    documents = a2ui.get("data")
    if not isinstance(documents, list) or not documents:
        raise AssertionError(f"A2UI DataPart has no messages: {a2ui}")
    create = documents[0].get("createSurface")
    if not isinstance(create, Mapping) or create.get("surfaceId") != "forecast-surface":
        raise AssertionError(f"unexpected A2UI createSurface: {documents[0]}")

    response_metadata = next(
        (
            value.get("metadata")
            for value in responses
            if isinstance(value, Mapping) and isinstance(value.get("metadata"), Mapping)
        ),
        None,
    )
    # Metadata may be nested in the normalized A2A message rather than the
    # top-level response, so fall back to a recursive search.
    if response_metadata is None:
        response_metadata = _find_message_metadata(responses)
    if not isinstance(response_metadata, Mapping) or response_metadata.get("source") != "example-11":
        raise AssertionError(f"SkillResult metadata was not preserved: {responses}")

    print("PASS  forecast returned business data + metadata + A2UI DataPart")


def _find_message_metadata(value: Any) -> Mapping[str, Any] | None:
    if isinstance(value, Mapping):
        metadata = value.get("metadata")
        if isinstance(metadata, Mapping) and metadata.get("source") == "example-11":
            return metadata
        for child in value.values():
            found = _find_message_metadata(child)
            if found is not None:
                return found
    elif isinstance(value, list | tuple):
        for child in value:
            found = _find_message_metadata(child)
            if found is not None:
                return found
    return None


def _assert_summary(responses: tuple[dict[str, object], ...]) -> None:
    parts = _find_parts(responses)
    if any(
        isinstance(part.get("metadata"), Mapping)
        and part["metadata"].get("mimeType") == A2UI_MIME_TYPE
        for part in parts
    ):
        raise AssertionError("ordinary summary unexpectedly returned an A2UI DataPart")
    if not any(
        isinstance(part.get("data"), Mapping)
        and part["data"].get("items") == 3
        for part in parts
    ):
        raise AssertionError(f"ordinary structured A2A result missing: {responses}")
    print("PASS  summary remains an ordinary non-A2UI A2A result")


async def main() -> None:
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        a2ui_config=config_path(HERE, "a2ui.conf"),
    )
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    try:
        card = await agent.resolve_agent_card(SERVER_URL)
        _assert_agent_card(card)
        provider = _direct_provider(card, SERVER_URL)

        forecast = await agent.send_message(
            provider,
            data={"region": "east"},
            skill_id="forecast",
        )
        _assert_forecast(forecast)

        summary = await agent.send_message(
            provider,
            data={},
            skill_id="summary",
        )
        _assert_summary(summary)

        print("RESULT: A2A + A2UI v1.0 acceptance verification passed")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
