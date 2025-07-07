from fastapi import FastAPI, Request, Response
import httpx
from cache import get_cache_response, set_cached_response
import uvicorn

app = FastAPI()
origin_url = ""

def start_proxy_server(port:int, origin:str):
    global origin_url
    origin_url = origin.rstrip("/")
    uvicorn.run("server.app", host="0.0.0.0", port=port,reload=False)

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT","DELETE","PATCH"])
async def handle_requests(request:Request, full_path:str):
    global origin_url
    
    method = request.method
    query_string = str(request.url.query)