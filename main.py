from fastapi import FastAPI
import time
from caching import init_cache, cache_if_enabled
from config import settings
from fastapi_cache import FastAPICache

app = FastAPI()

@app.on_event("startup")
def startup():
    """Initialize cache globally at startup."""
    init_cache()

@app.get("/nocache")
async def no_cache():
    """An endpoint without caching."""
    time.sleep(2)  # Simulate expensive computation
    return {"message": "No cache applied", "timestamp": time.time()}

@app.get("/cache")
@cache_if_enabled(expire=10)  # Automatically applies caching if enabled
async def cached_endpoint():
    """An endpoint that uses caching only if it's enabled."""
    time.sleep(2)
    return {"message": "Cached response", "timestamp": time.time()}

@app.get("/custom/{item_id}")
@cache_if_enabled(expire=10)
async def custom_cache(item_id: int):
    """Caches per item_id dynamically."""
    time.sleep(2)
    return {"message": f"Cached data for item {item_id}", "timestamp": time.time()}

@app.get("/clear-cache")
async def clear_cache():
    """Manually clear the cache if enabled."""
    if settings.ENABLE_CACHE:
        await FastAPICache.clear()
        return {"message": "Cache cleared"}
    return {"message": "Cache is disabled, nothing to clear"}
