import asyncio
from types import SimpleNamespace
from app.core import rate_limit


def test_rate_limit_blocks_after_limit(monkeypatch):
    rate_limit._buckets.clear()
    request = SimpleNamespace(method="GET", url=SimpleNamespace(path="/products"), client=SimpleNamespace(host="1.2.3.4"))
    calls = 0
    async def call_next(_):
        nonlocal calls
        calls += 1
        return "ok"

    async def run():
        first = await rate_limit.rate_limit_middleware(request, call_next, 1, 60)
        second = await rate_limit.rate_limit_middleware(request, call_next, 1, 60)
        return first, second

    first, second = asyncio.run(run())
    assert first == "ok"
    assert second.status_code == 429
    assert calls == 1
