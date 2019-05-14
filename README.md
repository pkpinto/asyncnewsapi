# asyncnewsapi

An asyncio Python library to perform request against [News API](https://newsapi.org). It provides direct access to the endpoints defined in the [documentation](https://newsapi.org/docs/endpoints).

It's loosely based on [newsapi-python](https://github.com/mattlisiv/newsapi-python), a requests based library by Matt Lisivick.

The api.key file present in the repo is encrypted using [git-crypt](https://github.com/AGWA/git-crypt). Go to News API [website](https://newsapi.org) to create a free API key and replace the contents of this file.


## Tests

Unit tests for the Session class have been implemented. These can run using:
```
python -m unittest asyncnewsapi/tests/test_session.py 
```
from the root of the repo.