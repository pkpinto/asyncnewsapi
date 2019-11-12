import asyncio

import aiohttp
from async_timeout import timeout
import pytest

from asyncnewsapi import Session
from tests import async_test


class TestSession:

    @async_test
    async def test_loop(self):
        async with Session() as api:
            assert isinstance(api.loop, asyncio.AbstractEventLoop)

    @async_test
    async def test_reuse_loop(self):
        loop = asyncio.get_event_loop()
        async with Session(loop=loop) as api:
            assert api.loop == loop

    @async_test
    async def test_api_key_correct(self):
        async with Session() as api:
            async for r in api.top_headlines(language='en'):
                assert 'title' in r.keys()
                break

    @async_test
    async def test_api_key_incorrect(self):
        async with Session(api_key='1' * 32) as api:
            with pytest.raises(aiohttp.client_exceptions.ClientResponseError):
                async for r in api.top_headlines(language='en'):
                    break

    @async_test
    async def test_timeout_inner_timeout_error(self):
        with pytest.raises(asyncio.TimeoutError):
            # do not give the task enough time to complete
            async with Session(timeout=0.001) as api:
                async for r in api.top_headlines(language='en'):
                    break
