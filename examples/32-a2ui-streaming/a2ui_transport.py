"""Native A2A DataPart helper for application-owned A2UI stream messages."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from a2a.helpers import new_data_part
from a2a.types import Part


# -----------------------------------------------------------------------------
# A2UI transport constants
# -----------------------------------------------------------------------------

A2UI_MIME_TYPE = "application/a2ui+json"


# -----------------------------------------------------------------------------
# Native A2A Part construction
# -----------------------------------------------------------------------------

def a2ui_part(messages: list[dict]) -> Part:
    """Carry ordered A2UI protocol documents in a native A2A DataPart."""

    return new_data_part(
        {"messages": messages},
        media_type=A2UI_MIME_TYPE,
    )
