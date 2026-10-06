"""Application-owned mixed Basic + Rich A2UI presentation."""
from __future__ import annotations

import copy
import json
from pathlib import Path

A2UI_VERSION = "v1.0"
BASIC_CATALOG_ID = (
    "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
)
RICH_CATALOG_ID = "https://agentnebula.ai/catalogs/a2ui/rich/v1/catalog.json"
SURFACE_ID = "weather-dashboard-surface"


class WeatherDashboardPresenter:
    """Bind weather data without interpreting Basic or Rich components.

    ``presentation.json`` owns the complete component tree and identifies Rich
    components with their catalog ID. The presenter only supplies application
    data and the standard A2UI createSurface envelope.
    """

    def __init__(self, manifest_path: Path) -> None:
        self._manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    def create_surface(
        self,
        *,
        region: str,
        temperature: int,
        humidity: int,
        wind_speed: int,
        conditions: str,
    ) -> dict:
        """Return one mixed-catalog A2UI v1.0 surface."""
        manifest = copy.deepcopy(self._manifest)
        data_model = dict(manifest.get("dataModel", {}))
        data_model.update(
            {
                "region": region,
                "status": {"label": conditions},
                "metrics": [
                    {"label": "Temperature", "value": temperature, "unit": "°F"},
                    {"label": "Humidity", "value": humidity, "unit": "%"},
                    {"label": "Wind", "value": wind_speed, "unit": "mph"},
                ],
                "summary": f"{conditions} conditions across {region}.",
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
