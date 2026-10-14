"""Load the application-owned A2UI presentation for Example 33."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import copy
import json
from pathlib import Path


# -----------------------------------------------------------------------------
# Presentation
# -----------------------------------------------------------------------------

def load_presentation(path: Path, data_model: dict) -> dict:
    """Load the presentation JSON and bind runtime business data."""

    document = copy.deepcopy(json.loads(path.read_text(encoding="utf-8")))
    document["createSurface"]["dataModel"] = data_model
    return document
