"""Load the negotiated application-owned A2UI v1.0 message from JSON."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations

import copy
import json
from pathlib import Path

# -----------------------------------------------------------------------------
# Presentation loading
# -----------------------------------------------------------------------------
def load_presentation(path: Path, supported_catalog_ids: list[str]) -> dict[str, object]:
    """Select a complete JSON-defined presentation for a mutually supported catalog."""
    manifest = json.loads(path.read_text(encoding="utf-8"))
    presentations = manifest.get("presentations", {})
    for catalog_id in supported_catalog_ids:
        document = presentations.get(catalog_id)
        if document is not None:
            return copy.deepcopy(document)
    raise ValueError("renderer did not advertise a mutually supported A2UI catalog")
