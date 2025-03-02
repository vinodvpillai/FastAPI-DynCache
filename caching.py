from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend
from pymemcache.client.base import Client as MemcacheClient
from fastapi_cache.decorator import cache
from config import settings
from fastapi_cache.backends.inmemory import InMemoryBackend
import functools

def init_cache():
    """Initialize caching backend only if caching is enabled."""
    if settings.ENABLE_CACHE:
        if settings.CACHE_BACKEND == "memcached":
            memcached_client = MemcacheClient((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
            FastAPICache.init(MemcachedBackend(memcached_client), prefix="fastapi-cache")
        else:
            FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")  # Default

    else:
        print("Caching is DISABLED. Skipping cache initialization.")

def cache_if_enabled(expire: int):
    """
    A decorator that applies caching only if ENABLE_CACHE is True.
    Otherwise, it executes the function normally.
    """
    def decorator(func):
        if settings.ENABLE_CACHE:
            return cache(expire=expire)(func)
        return functools.wraps(func)(func)  # Return original function if caching is disabled
    return decorator
