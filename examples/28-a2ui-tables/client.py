import asyncio
from pathlib import Path
from a2a_client import request_surface
HERE=Path(__file__).resolve().parent
def messages(message):
    return next(p["data"]["messages"] for p in message["parts"] if p.get("media_type")=="application/a2ui+json")
async def main():
    docs=messages(await request_surface(HERE)); create=next(x["createSurface"] for x in docs if "createSurface" in x); assert create["surfaceId"]=="inventory-table-surface"; print("PASS  A2UI table surface returned over native A2A"); print("RESULT: Example 28 passed")
if __name__=="__main__": asyncio.run(main())
