"""Application-owned A2UI presentation for the interactive counter."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from typing import Any
A2UI_VERSION = "v1.0"
BASIC_CATALOG = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
SURFACE_ID = "counter-surface"

class CounterPresenter:
    """Load the JSON manifest and create standard A2UI v1.0 messages."""
    def __init__(self, manifest_path: Path) -> None:
        self._manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    def create_surface(self, count: int) -> dict[str, Any]:
        """Create the initial surface; component semantics stay in JSON."""
        manifest = copy.deepcopy(self._manifest)
        data_model = manifest.get("dataModel", {})
        data_model["count"] = count
        return {"version": A2UI_VERSION, "createSurface": {"surfaceId": SURFACE_ID, "catalogId": BASIC_CATALOG, "sendDataModel": True, "components": manifest["components"], "dataModel": data_model}}

    @staticmethod
    def update_count(count: int) -> dict[str, Any]:
        """Return a standard incremental A2UI data-model update."""
        return {"version": A2UI_VERSION, "updateDataModel": {"surfaceId": SURFACE_ID, "path": "/count", "value": count}}
