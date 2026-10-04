"""Application-owned A2UI presentation loading and data binding."""
from __future__ import annotations

import copy
import json
from pathlib import Path

A2UI_VERSION = "v1.0"
BASIC_CATALOG_ID = (
    "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
)
SURFACE_ID = "forecast-surface"


class ForecastPresenter:
    """Create the forecast surface from the declarative presentation manifest.

    The JSON file owns the component tree and initial data model. This class
    adds invocation data and the standard A2UI surface envelope required on the
    wire. It does not interpret component types or duplicate catalog behavior.
    """

    def __init__(self, manifest_path: Path) -> None:
        self._manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    def create_surface(
        self,
        *,
        region: str,
        temperature: str,
        conditions: str,
    ) -> dict:
        """Return one A2UI v1.0 createSurface document for this invocation."""
        manifest = copy.deepcopy(self._manifest)
        data_model = dict(manifest.get("dataModel", {}))
        data_model.update(
            {
                "region": region,
                "temperature": temperature,
                "conditions": conditions,
            }
        )

        return {
            "version": A2UI_VERSION,
            "createSurface": {
                "surfaceId": SURFACE_ID,
                "catalogId": BASIC_CATALOG_ID,
                "sendDataModel": True,
                "components": manifest["components"],
                "dataModel": data_model,
            },
        }
