from fastapi import FastAPI, Request, Response
import httpx
from cache import get_cache_response, set_cache_response
import uvicorn
import logging


logger = logging.getLogger(__name__)


app = FastAPI()
origin_url = ""

def start_proxy_server(port:int, origin:str):
    global origin_url
    origin_url = origin.rstrip("/")
    logger.debug("Starting proxy Server")
    print("Starting Proxy Server")
    uvicorn.run(app=app, host="0.0.0.0", port=port,reload=False)


@app.middleware("http")
async def log_requests(request:Request, call_next):
    print(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response
    


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT","DELETE","PATCH"])
async def handle_requests(request:Request, full_path:str):
    global origin_url
    
    method = request.method
    logger.info("The method for the request sent is %s", method)
    query_string = str(request.url.query)
    path = f"{full_path}?{query_string}" if query_string else full_path
    logger.debug("This is the full Path %s", full_path)
    url = f"{origin_url}/{path}"
    
    
    cache_key = f"{method}:{url}"
    logger.debug("Cached Key is %s", cache_key)
    
    # Check Cache
    cached_response = get_cache_response(cache_key)
    if cached_response:
        return Response(
            content=cached_response["content"],
            status_code=cached_response["status_code"],
            headers={**cached_response["headers"], "X-cache": "HIT"}
        )
        
    # Forward to origin if not cached
    async with httpx.AsyncClient(follow_redirects=False) as client:
        forwarded_response = await client.request(
            method=method,
            url=url,
            headers={key:value for key, value in request.headers.items() if key.lower() != "host"},
            content= await request.body()
        )
    
    content = forwarded_response.content
    status_code = forwarded_response.status_code
    headers = dict(forwarded_response.headers)
    
    if status_code in (301,302, 303, 307,308):
        redirect_url = headers.get("location")
        if redirect_url:
            print(f"Following redirect to {redirect_url}")
            async with httpx.AsyncClient() as client:
                redirected_response = await client.request("GET", redirect_url)
                content = redirected_response.content
                status_code = redirected_response.status_code
                headers = dict(redirected_response.headers)
                
    # Rewrite Location header if it's a redirect
    if "location" in headers and headers["location"].startswith(origin_url):
        headers["location"] = headers["location"].replace(origin_url, "http://localhost:3001")
    
    # Cache response only if it's not a redirect (optional)
    if not (300 <= status_code < 400):
            set_cache_response(cache_key, content, headers, status_code)
            
    headers["X-Cache"] = "Miss"
        
    return Response(content=content, status_code=status_code, headers=headers)