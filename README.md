# asyncnewsapi

[![Build Status](https://travis-ci.org/pkpinto/asyncnewsapi.svg?branch=master)](https://travis-ci.com/pkpinto/asyncnewsapi)
[![Code Coverage](https://codecov.io/gh/pkpinto/asyncnewsapi/branch/master/graph/badge.svg)](https://codecov.io/gh/pkpinto/asyncnewsapi)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

An asyncio Python library to perform request against [News API](https://newsapi.org). It provides direct access to the endpoints defined in the [documentation](https://newsapi.org/docs/endpoints), returning async iterators for the request results. A minimal implementation can be as simple as:
```
import asyncio
from asyncnewsapi.session import Session

async def main():
    async with Session() as api:
        i = 1
        async for article in api.top_headlines(language='pt'):
            print('{}: {}'.format(i, article['title']))
            i += 1

if __name__ == '__main__':
    asyncio.run(main())
```

The API key should be provided as an environment variable named NEWSAPI_KEY:
```
export NEWSAPI_KEY="..."
```
Go to News API [website](https://newsapi.org) to create a free API key.

This library is loosely based on / inspired by [newsapi-python](https://github.com/mattlisiv/newsapi-python), a requests based library by Matt Lisivick.

## Tests

Unit tests for the Session class have been implemented using pytest. These can run using:
```
pytest -v
```
from the root of the repo.
