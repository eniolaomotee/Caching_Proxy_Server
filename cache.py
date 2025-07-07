cache = {}

def get_cache_response(key:str):
    return cache.get(key)

def set_cache_response(key:str, content:bytes,headers:dict, status_code:int):
    cache[key] = {
        "content":content,
        "status_code": status_code,
        "headers": headers
    }
    
def clear_cache():
    cache.clear()
    
    