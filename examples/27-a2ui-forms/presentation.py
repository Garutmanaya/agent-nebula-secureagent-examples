"""Application-owned A2UI presentation for the contact form example."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

A2UI_VERSION = "v1.0"
BASIC_CATALOG = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
SURFACE_ID = "contact-form-surface"


class ContactFormPresenter:
    """Load the JSON manifest and produce standard A2UI v1.0 messages."""

    def __init__(self, manifest_path: Path) -> None:
        self._manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    def create_surface(self) -> dict[str, Any]:
        """Create the initial form surface from the application manifest."""
        manifest = copy.deepcopy(self._manifest)
        return {
            "version": A2UI_VERSION,
            "createSurface": {
                "surfaceId": SURFACE_ID,
                "catalogId": BASIC_CATALOG,
                "sendDataModel": True,
                "components": manifest["components"],
                "dataModel": manifest.get("dataModel", {}),
            },
        }

    @staticmethod
    def update_result(result: str) -> dict[str, Any]:
        """Update only the result while preserving browser-entered values."""
        return {
            "version": A2UI_VERSION,
            "updateDataModel": {
                "surfaceId": SURFACE_ID,
                "path": "/result",
                "value": result,
            },
        }
