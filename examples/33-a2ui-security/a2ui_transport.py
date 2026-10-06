"""A2UI JSON documents carried by a native A2A DataPart."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from a2a.helpers import new_data_part
from a2a.types import Part


# -----------------------------------------------------------------------------
# A2UI transport
# -----------------------------------------------------------------------------

A2UI_MIME_TYPE = "application/a2ui+json"


def a2ui_part(messages: list[dict]) -> Part:
    """Wrap application-owned A2UI messages in a native A2A DataPart."""

    return new_data_part(
        {"messages": messages},
        media_type=A2UI_MIME_TYPE,
    )
