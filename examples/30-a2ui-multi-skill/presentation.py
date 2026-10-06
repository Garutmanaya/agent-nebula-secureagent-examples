from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import copy
import json
from pathlib import Path


# -----------------------------------------------------------------------------
# Presentation loading
# -----------------------------------------------------------------------------

def load_presentation(path: Path, data_model: dict) -> dict:
    """Load an application-owned A2UI presentation and overlay runtime data."""

    document = copy.deepcopy(
        json.loads(path.read_text(encoding="utf-8"))
    )
    document["createSurface"]["dataModel"] = data_model

    return document
