import asyncio


# async test decorator - https://stackoverflow.com/a/46324983
def async_test(coro):
    def wrapper(*args, **kwargs):
        asyncio.run(coro(*args, **kwargs))
    return wrapper
