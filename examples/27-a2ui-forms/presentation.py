"""Load application-owned complete A2UI v1.0 protocol messages from JSON."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations
import copy
import json
from pathlib import Path
from typing import Any

SURFACE_ID = "contact-form-surface"

# -----------------------------------------------------------------------------
# Presentation loading
# -----------------------------------------------------------------------------
class ContactFormPresenter:
    """Load complete protocol documents; Python only binds runtime values."""
    def __init__(self, path: Path) -> None:
        self._documents = json.loads(path.read_text(encoding="utf-8"))

    def create_surface(self) -> dict[str, Any]:
        document = copy.deepcopy(self._documents["initial"])

        return document

    def update_result(self, value: str) -> dict[str, Any]:
        document = copy.deepcopy(self._documents["update"])
        document["updateDataModel"]["value"] = value
        return document
