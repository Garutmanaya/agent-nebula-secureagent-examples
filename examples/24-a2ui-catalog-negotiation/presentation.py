"""Application-owned A2UI v1.0 catalog selection for Example 24."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import annotations

BASIC_CATALOG_ID = "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
RICH_CATALOG_ID = "https://agentnebula.ai/catalogs/a2ui/rich/v1/catalog.json"


def create_surface(supported_catalog_ids: list[str]) -> dict[str, object]:
    """Select the best mutually supported catalog for this surface."""
    if RICH_CATALOG_ID in supported_catalog_ids:
        catalog_id = RICH_CATALOG_ID
        components = [
            {"id": "root", "component": "Column", "children": ["title", "status"]},
            {"id": "title", "component": "Text", "text": "Catalog negotiation"},
            {"id": "status", "component": "StatusBadge", "label": "Rich catalog selected", "status": "success"},
        ]
    elif BASIC_CATALOG_ID in supported_catalog_ids:
        catalog_id = BASIC_CATALOG_ID
        components = [
            {"id": "root", "component": "Column", "children": ["title", "status"]},
            {"id": "title", "component": "Text", "text": "Catalog negotiation"},
            {"id": "status", "component": "Text", "text": "Basic catalog selected"},
        ]
    else:
        raise ValueError("renderer did not advertise a mutually supported A2UI catalog")

    return {
        "version": "v1.0",
        "createSurface": {
            "surfaceId": "catalog-negotiation-surface",
            "catalogId": catalog_id,
            "components": components,
            "dataModel": {"selectedCatalogId": catalog_id},
        },
    }
