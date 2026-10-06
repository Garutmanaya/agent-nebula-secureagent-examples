import asyncio
from pathlib import Path
from a2a_client import request_surface
HERE=Path(__file__).resolve().parent
def surface(message):
    docs=next(p["data"]["messages"] for p in message["parts"] if p.get("media_type")=="application/a2ui+json"); return next(x["createSurface"] for x in docs if "createSurface" in x)
async def main():
    a=surface(await request_surface(HERE,"inventory")); b=surface(await request_surface(HERE,"traffic")); assert a["surfaceId"]!=b["surfaceId"]; print("PASS  different native A2A skills produced different A2UI surfaces"); print("RESULT: Example 30 passed")
if __name__=="__main__": asyncio.run(main())
