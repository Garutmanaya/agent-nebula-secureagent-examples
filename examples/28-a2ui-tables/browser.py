from __future__ import annotations
import asyncio,json
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from a2a_client import request_surface
HERE=Path(__file__).resolve().parent; DIST=HERE.parents[1]/"examples"/"common"/"a2ui-web"/"dist"
def extract(message): return next(p["data"]["messages"] for p in message["parts"] if p.get("media_type")=="application/a2ui+json")
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a,directory=str(DIST),**k)
    def do_GET(self):
        if urlparse(self.path).path=="/api/a2ui":
            body=json.dumps({"messages":extract(asyncio.run(request_surface(HERE)))}).encode(); self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().do_GET()
if __name__=="__main__": print("Browser validation: http://localhost:9128"); ThreadingHTTPServer(("0.0.0.0",9128),Handler).serve_forever()
