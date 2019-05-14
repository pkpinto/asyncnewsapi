import asyncio
import sys


try:
    with open('api.key') as f:
        APIKEY = f.read()
except FileNotFoundError as e:
    print('api.key file containing API key is missing from root of repo. '
          'Go to https://newsapi.org to create a free API key.', file=sys.stderr)
    sys.exit()


# async test decorator - https://stackoverflow.com/a/46324983
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper
