"""A2UI JSON documents carried by native A2A DataParts."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from a2a.helpers import new_data_part
from a2a.types import Part


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

A2UI_MIME_TYPE = "application/a2ui+json"


# -----------------------------------------------------------------------------
# A2UI transport
# -----------------------------------------------------------------------------

def a2ui_part(messages: list[dict]) -> Part:
    """Wrap A2UI protocol messages in a native A2A DataPart."""

    return new_data_part(
        {"messages": messages},
        media_type=A2UI_MIME_TYPE,
    )
