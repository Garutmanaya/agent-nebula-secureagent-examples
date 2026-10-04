"""A2UI v1.0 payload helpers using native a2a-sdk Parts only."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from a2a.helpers import new_data_part
from a2a.types import Part
from google.protobuf.json_format import MessageToDict
A2UI_MIME_TYPE = "application/a2ui+json"

def a2ui_part(messages: list[dict[str, Any]]) -> Part:
    """Carry ordered A2UI messages in a native A2A DataPart."""
    return new_data_part({"messages": messages}, media_type=A2UI_MIME_TYPE)

def a2ui_messages(message: Any) -> list[dict[str, Any]]:
    """Extract A2UI messages from a native A2A Message without translating them."""
    payload = MessageToDict(message, preserving_proto_field_name=True)
    for part in payload.get("parts", []):
        if part.get("media_type") != A2UI_MIME_TYPE:
            continue
        data = part.get("data", {})
        messages = data.get("messages", []) if isinstance(data, Mapping) else []
        return [item for item in messages if isinstance(item, dict)]
    return []
