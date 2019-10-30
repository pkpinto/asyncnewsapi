import aiohttp
import asyncio
from async_timeout import timeout

import pytest

from asyncnewsapi import Session
from asyncnewsapi.tests import async_test


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
            tasks = [api.top_headlines(language='en'), ]
            await asyncio.gather(*tasks)

    @async_test
    async def test_api_key_incorrect(self):
        async with Session(api_key='1' * 32) as api:
            tasks = [api.top_headlines(language='en'), ]
            with pytest.raises(aiohttp.client_exceptions.ClientResponseError):
                await asyncio.gather(*tasks)

    @async_test
    async def test_timeout_inner_timeout_error(self):
        with pytest.raises(asyncio.TimeoutError):
                async with Session(timeout=0.01) as api:
                    # something that will take a long time
                    tasks = [api.top_headlines(language='en'), ] * 100
                    await asyncio.gather(*tasks)
