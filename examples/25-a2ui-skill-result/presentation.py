"""Application-owned presentation loading for Example 25.

The presenter understands the example's manifest format only. It does not
interpret A2UI component types or catalogs; those remain A2UI concerns.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

A2UI_VERSION = "v1.0"
BASIC_CATALOG_ID = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"


class SkillPresenter:
    """Create one A2UI surface from an application-owned JSON manifest."""

    def __init__(self, manifest_path: Path, surface_id: str) -> None:
        self._manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self._surface_id = surface_id

    def create_surface(self, data_model: dict[str, object]) -> dict[str, object]:
        """Bind skill data without interpreting the manifest's components."""
        manifest = copy.deepcopy(self._manifest)
        return {
            "version": A2UI_VERSION,
            "createSurface": {
                "surfaceId": self._surface_id,
                "catalogId": BASIC_CATALOG_ID,
                "components": manifest["components"],
                "dataModel": data_model,
            },
        }
