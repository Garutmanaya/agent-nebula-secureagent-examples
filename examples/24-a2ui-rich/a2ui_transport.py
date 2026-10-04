"""A2UI-over-A2A wire helpers used only by this example application.

A2UI defines JSON protocol documents. A2A provides the transport. This module
uses native a2a-sdk helpers directly; it is not an Agent Nebula A2UI API.
"""
from a2a.helpers import new_data_part
from a2a.types import Part

A2UI_MIME_TYPE = "application/a2ui+json"


def a2ui_part(messages: list[dict]) -> Part:
    """Create a native A2A DataPart containing ordered A2UI documents."""
    return new_data_part({"messages": messages}, media_type=A2UI_MIME_TYPE)
