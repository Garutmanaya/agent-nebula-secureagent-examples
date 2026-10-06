import asyncio
from pathlib import Path
from a2a_client import request_surface
HERE=Path(__file__).resolve().parent
RICH_CATALOG_ID="https://agentnebula.ai/catalogs/a2ui/rich/v1/catalog.json"
def messages(message):
    return next(p["data"]["messages"] for p in message["parts"] if p.get("media_type")=="application/a2ui+json")
async def main():
    docs=messages(await request_surface(HERE)); create=next(x["createSurface"] for x in docs if "createSurface" in x)
    assert create["surfaceId"]=="traffic-chart-surface"
    assert create["catalogId"]==RICH_CATALOG_ID
    chart=next(component for component in create["components"] if component["component"]=="BarChart")
    assert chart["data"]=={"path":"/series"}
    print("PASS  Agent Nebula Rich Catalog BarChart returned over native A2A")
    print("RESULT: Example 29 passed")
if __name__=="__main__": asyncio.run(main())
