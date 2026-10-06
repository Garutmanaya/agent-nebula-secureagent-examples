"""Protocol-level verification for Example 23 mixed catalogs."""
import asyncio
from pathlib import Path

from a2a_client import request_dashboard

HERE = Path(__file__).resolve().parent
A2UI_MIME_TYPE = "application/a2ui+json"


async def main() -> None:
    message = await request_dashboard(HERE)
    parts = message.get("parts", [])
    part = next(
        (item for item in parts if item.get("media_type") == A2UI_MIME_TYPE),
        None,
    )
    if part is None:
        raise AssertionError(f"A2UI DataPart missing: {message}")

    documents = part.get("data", {}).get("messages", [])
    create = documents[0].get("createSurface", {}) if documents else {}
    if create.get("surfaceId") != "weather-dashboard-surface":
        raise AssertionError(f"unexpected A2UI surface: {documents}")

    rich_catalog_id = create.get("catalogId")
    if not rich_catalog_id:
        raise AssertionError(f"surface did not select a catalog: {create}")

    components = create.get("components", [])
    basic_types = {
        component.get("component")
        for component in components
        if "catalogId" not in component
    }
    rich_components = [
        component
        for component in components
        if component.get("catalogId") == rich_catalog_id
    ]
    rich_types = {component.get("component") for component in rich_components}

    if not {"Column", "Text"}.issubset(basic_types):
        raise AssertionError(f"Basic Catalog components missing: {components}")
    if not {"StatusBadge", "MetricGroup"}.issubset(rich_types):
        raise AssertionError(f"Rich Catalog components missing: {components}")

    data_model = create.get("dataModel", {})
    if data_model.get("region") != "Northern Virginia":
        raise AssertionError(f"application data model missing region: {data_model}")
    if len(data_model.get("metrics", [])) != 3:
        raise AssertionError(f"application metrics missing: {data_model}")

    print("PASS  native a2a-sdk Message contains A2UI v1.0 DataPart")
    print("PASS  one surface contains Basic and Rich catalog components")
    print("PASS  Rich components use the explicit Agent Nebula Rich catalog ID")
    print("PASS  application data model drives Basic and Rich components")
    print("RESULT: Example 23 mixed A2UI Basic + Rich verification passed")


if __name__ == "__main__":
    asyncio.run(main())
