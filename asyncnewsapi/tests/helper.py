import asyncio
import os
import sys


APIKEY = os.environ.get('NEWSAPI_KEY')
if not APIKEY:
    print('The NEWSAPI_KEY environment variable is not set, it should contain the API key. '
          'Go to https://newsapi.org to create a free API key.', file=sys.stderr)
    sys.exit()


# async test decorator - https://stackoverflow.com/a/46324983
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper
