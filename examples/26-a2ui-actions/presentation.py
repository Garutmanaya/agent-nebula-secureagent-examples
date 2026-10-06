"""Load application-owned complete A2UI v1.0 protocol messages from JSON."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
import copy
import json
from pathlib import Path
from typing import Any

SURFACE_ID = "counter-surface"

# -----------------------------------------------------------------------------
# Presentation loading
# -----------------------------------------------------------------------------
class CounterPresenter:
    """Load complete protocol documents; Python only binds runtime values."""
    def __init__(self, path: Path) -> None:
        self._documents = json.loads(path.read_text(encoding="utf-8"))

    def create_surface(self, count: int) -> dict[str, Any]:
        document = copy.deepcopy(self._documents["initial"])
        document["createSurface"]["dataModel"]["count"] = count
        return document

    def update_count(self, value: int) -> dict[str, Any]:
        document = copy.deepcopy(self._documents["update"])
        document["updateDataModel"]["value"] = value
        return document
