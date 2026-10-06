"""Load application-owned A2UI v1.0 protocol messages from JSON."""
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
def load_presentation(path: Path, data_model: dict[str, object]) -> dict[str, object]:
    """Load one complete A2UI message and bind invocation-specific data only."""
    document = copy.deepcopy(json.loads(path.read_text(encoding="utf-8")))
    create_surface = document.get("createSurface")
    if not isinstance(create_surface, dict):
        raise ValueError(f"{path} must contain one A2UI v1.0 createSurface message")
    model = dict(create_surface.get("dataModel", {}))
    model.update(data_model)
    create_surface["dataModel"] = model
    return document
