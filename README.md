# asyncnewsapi

An asyncio Python library to perform request against [News API](https://newsapi.org). It provides direct access to the endpoints defined in the [documentation](https://newsapi.org/docs/endpoints).

It's loosely based on [newsapi-python](https://github.com/mattlisiv/newsapi-python), a requests based library by Matt Lisivick.

The API key should be provided as an environment variable named NEWSAPI_KEY:
```
export NEWSAPI_KEY="..."
```
Go to News API [website](https://newsapi.org) to create a free API key.


## Tests

Unit tests for the Session class have been implemented using pytest. These can run using:
```
pytest -v
```
from the root of the repo.
