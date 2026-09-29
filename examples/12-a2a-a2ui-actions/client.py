"""Verify A2UI v1.0 renderer actions over the standard A2A binding."""
from __future__ import annotations

import asyncio
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from examples.example_paths import config_path
from agent_nebula_secureagent import SecureAgent

HERE = Path(__file__).resolve().parent
SERVER_URL = "http://localhost:9012/"
SURFACE_ID = "forecast-action-surface"
A2UI_MIME_TYPE = "application/a2ui+json"


def _parts(value: Any) -> list[Mapping[str, Any]]:
    result: list[Mapping[str, Any]] = []
    if isinstance(value, Mapping):
        parts = value.get("parts")
        if isinstance(parts, list):
            result.extend(part for part in parts if isinstance(part, Mapping))
        for child in value.values():
            result.extend(_parts(child))
    elif isinstance(value, list | tuple):
        for child in value:
            result.extend(_parts(child))
    return result


def _a2ui_documents(value: Any) -> list[Mapping[str, Any]]:
    documents: list[Mapping[str, Any]] = []
    for part in _parts(value):
        metadata = part.get("metadata")
        if not isinstance(metadata, Mapping) or metadata.get("mimeType") != A2UI_MIME_TYPE:
            continue
        data = part.get("data")
        if isinstance(data, list):
            documents.extend(item for item in data if isinstance(item, Mapping))
    return documents


def _business_units(value: Any) -> int | None:
    for part in _parts(value):
        data = part.get("data")
        metadata = part.get("metadata")
        if isinstance(data, Mapping) and not (
            isinstance(metadata, Mapping) and metadata.get("mimeType") == A2UI_MIME_TYPE
        ):
            units = data.get("units")
            if isinstance(units, int | float):
                return int(units)
    return None


async def main() -> None:
    agent = SecureAgent(
        config=config_path(HERE, "secureagent.conf"),
        a2ui_config=config_path(HERE, "a2ui.conf"),
    )
    agent.use_protocol("a2a", role="client", config=config_path(HERE, "a2aclient.conf"))
    try:
        initial = await agent.send_message_to(SERVER_URL, data={})
        if _business_units(initial) != 1250:
            raise AssertionError(f"initial forecast missing: {initial}")
        if not any("createSurface" in document for document in _a2ui_documents(initial)):
            raise AssertionError("initial A2UI surface missing")
        print("PASS  provider returned the interactive A2UI v1.0 surface")

        updated = await agent.send_a2ui_action(
            SERVER_URL,
            name="recalculate",
            surface_id=SURFACE_ID,
            source_component_id="button",
            context={"delta": 50},
            data_model={"units": 1250},
            want_response=True,
            action_id="recalculate-1",
        )
        if _business_units(updated) != 1300:
            raise AssertionError(f"recalculated business result missing: {updated}")
        documents = _a2ui_documents(updated)
        response = next((doc for doc in documents if "actionResponse" in doc), None)
        if response is None or response.get("actionId") != "recalculate-1":
            raise AssertionError(f"correlated actionResponse missing: {documents}")
        update = next((doc for doc in documents if "updateDataModel" in doc), None)
        if not isinstance(update, Mapping) or update["updateDataModel"].get("value") != 1300:
            raise AssertionError(f"updated A2UI data model missing: {documents}")
        print("PASS  renderer action reached the provider over A2A")
        print("PASS  renderer data model reached the surface owner")
        print("PASS  provider returned correlated actionResponse + updated A2UI")
        print("RESULT: bidirectional A2UI v1.0 action verification passed")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
