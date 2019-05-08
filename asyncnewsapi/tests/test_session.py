import aiohttp
import asyncio
from unittest import TestCase

from asyncnewsapi.session import Session
from asyncnewsapi.tests.helper import APIKEY, async_test


class SessionTest(TestCase):

    @async_test
    async def test_loop(self):
        async with Session(api_key=APIKEY) as api:
            self.assertTrue(isinstance(api.loop, asyncio.AbstractEventLoop))

    @async_test
    async def test_api_key_correct(self):
        async with Session(api_key=APIKEY) as api:
            tasks = [api.top_headlines(language='en'), ]
            await asyncio.gather(*tasks)

    @async_test
    async def test_api_key_incorrect(self):
        async with Session(api_key='1' * len(APIKEY)) as api:
            tasks = [api.top_headlines(language='en'), ]
            with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
                await asyncio.gather(*tasks)
