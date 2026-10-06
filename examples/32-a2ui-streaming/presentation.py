"""Load complete application-owned A2UI streaming protocol messages."""

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

class StreamingTrafficPresenter:
    """Load A2UI documents while Python binds only runtime business data."""

    def __init__(self, path: Path) -> None:
        self._documents = json.loads(path.read_text(encoding="utf-8"))

    def create_surface(self, series: list[dict]) -> dict:
        """Return the initial chart surface."""

        document = copy.deepcopy(self._documents["initial"])
        document["createSurface"]["dataModel"]["series"] = series
        return document

    def update_series(self, series: list[dict]) -> dict:
        """Return an incremental data-model update for the existing surface."""

        document = copy.deepcopy(self._documents["update"])
        document["updateDataModel"]["value"] = series
        return document
