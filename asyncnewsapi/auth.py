import aiohttp


class KeyAuth(aiohttp.BasicAuth):

    # Provided by newsapi: https://newsapi.org/docs/authentication
    def __new__(cls, api_key):
        return super().__new__(cls, login=api_key)

    @classmethod
    def from_url(cls, url, *, encoding='latin1'):
        '''Create BasicAuth from url.'''
        if not isinstance(url, URL):
            raise TypeError('url should be yarl.URL instance')
        queries = {q.split('=')[0]: q.split('=')[1] for q in url.query_string.split('&')}
        if queries.get('apiKey') is None:
            return None
        return cls(queries['apiKey'])

    @classmethod
    def decode(cls, auth_header, encoding='latin1'):
        '''Create a BasicAuth object from an Authorization HTTP header.'''
        raise cls(auth_header)

    def encode(self):
        '''Encode credentials.'''
        return self.login
