import asyncio
from collections import deque
import logging

from asyncnewsapi.session import Session


class Stream(Session):

    def __init__(self, every=60, api_key=None, loop=None, timeout=None):
        self.every = every
        self.article_queue_maxlen = 1000
        super().__init__(api_key=api_key, loop=loop, timeout=timeout)

    async def top_headlines(self, **kwargs):
        logger = logging.getLogger(__name__)
        article_queue = deque(maxlen=self.article_queue_maxlen)
        while True:
            async for article in super().top_headlines(**kwargs):
                # the article hash is just the title
                article_hash = article['title']
                if article_hash in article_queue:
                    logger.debug('Bypassing repeat article: {}'.format(article_hash))
                    continue
                else:
                    article_queue.append(article_hash)
                    logger.debug('Append article to article_queue, current length: {}'.format(len(article_queue)))
                    yield article
            await asyncio.sleep(self.every)

    async def everything(self, **kwargs):
        logger = logging.getLogger(__name__)
        article_queue = deque(maxlen=self.article_queue_maxlen)
        while True:
            async for article in super().everything(**kwargs):
                # the article hash is just the title
                article_hash = article['title']
                if article_hash in article_queue:
                    logger.debug('Bypassing repeat article: {}'.format(article_hash))
                    continue
                else:
                    article_queue.append(article_hash)
                    logger.debug('Append article to article_queue, current length: {}'.format(len(article_queue)))
                    yield article
            await asyncio.sleep(self.every)
