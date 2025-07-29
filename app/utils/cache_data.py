import functools
import time
from typing import Callable
from fastapi import Request
from cachetools import TTLCache

# Global cache instance (example)
cache = TTLCache(maxsize=100, ttl=60)

def custom_cache(ttl: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            cache_key = f"{func.__name__}:{request.url.path if request else 'unknown'}"

            if cache_key in cache:
                start_time = time.perf_counter()
                result = cache[cache_key]
                end_time = time.perf_counter()
                time_taken_ms = (end_time - start_time) * 1000
                print(f"😎 Time taken by get the data from cache: {time_taken_ms:.3f} ms")
                return result

            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            time_taken_ms = (end_time - start_time) * 1000
            print(f"😎 Time taken by get the data from database: {time_taken_ms:.3f} ms")

            cache[cache_key] = result
            return result

        return wrapper
    return decorator