from collections import defaultdict, deque
from time import monotonic
from threading import Lock

from fastapi import Request
from fastapi.responses import JSONResponse

_buckets = defaultdict(deque)
_lock = Lock()

async def rate_limit_middleware(request: Request, call_next, limit: int, window: int):
    if request.url.path in {"/healthz", "/docs", "/openapi.json", "/redoc"}:
        return await call_next(request)
    key = request.client.host if request.client else "unknown"
    now = monotonic()
    with _lock:
        bucket = _buckets[key]
        while bucket and now - bucket[0] >= window:
            bucket.popleft()
        if len(bucket) >= limit:
            return JSONResponse(status_code=429, content={"detail": "Too many requests. Please try again later."})
        bucket.append(now)
    return await call_next(request)
