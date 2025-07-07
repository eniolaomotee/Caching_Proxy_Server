import time 
import logging 

logger = logging.getLogger(__name__)
cache_store = {}
CACHE_TTL_SECONDS = 300

def get_cache_response(key:str):
    cached = cache_store.get(key)
    logger.debug("The cached is %s", cached)
    if not cached:
        return None
    
    if time.time() - cached["timestamp"] > CACHE_TTL_SECONDS:
        del cache_store[key]
        return None
    
    
    return cached

def set_cache_response(key:str, content:bytes,headers:dict, status_code:int):
    cache_store[key] = {
        "content":content,
        "status_code": status_code,
        "headers": headers,
        "timestamp": time.time()
    }
    
def clear_cache():
    cache_store.clear()
    
    