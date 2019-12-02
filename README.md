# asyncnewsapi

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/pkpinto/asyncnewsapi.svg?branch=master)](https://travis-ci.org/pkpinto/asyncnewsapi)
[![PyPI version](https://badge.fury.io/py/asyncnewsapi.svg)](https://badge.fury.io/py/asyncnewsapi)
[![Code Coverage](https://codecov.io/gh/pkpinto/asyncnewsapi/branch/master/graph/badge.svg)](https://codecov.io/gh/pkpinto/asyncnewsapi)
[![Join the chat at https://gitter.im/asyncnewsapi/community](https://badges.gitter.im/asyncnewsapi/community.svg)](https://gitter.im/asyncnewsapi/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

An asyncio Python library to perform request against [News API](https://newsapi.org). It provides direct access to the endpoints defined in the [documentation](https://newsapi.org/docs/endpoints). 

Two classes are implemented, returning async iterators for the request results. Session will return an iterator through the results of a single request. Alternatively, Stream will return an infinite iterator, performing successive requests and continuing to iterate through the results. A minimal implementation can be as simple as:
```
import asyncio

from asyncnewsapi import Session

async def main():
    async with Session() as api:
        async for article in api.top_headlines(language='en'):
            print(article['title'])

if __name__ == '__main__':
    asyncio.run(main())
```

The API key should be provided as an environment variable named NEWSAPI_KEY:
```
export NEWSAPI_KEY="..."
```
Go to the NewsAPI [website](https://newsapi.org) to create a free API key.

This library is loosely based on / inspired by [newsapi-python](https://github.com/mattlisiv/newsapi-python), a requests based library by Matt Lisivick.

## Tests

Unit tests for the Session class have been implemented using pytest. These can run using:
```
pytest -v tests/
```
from the root of the repo (running it explicitly on the tests/ directory avoids interference with the venv folders).
