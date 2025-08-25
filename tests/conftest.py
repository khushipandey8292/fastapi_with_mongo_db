import pytest
import asyncio

@pytest.fixture(scope="function")
def event_loop():
    """Har test ke liye naya event loop banega (Motor ke liye zaruri hai)."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
