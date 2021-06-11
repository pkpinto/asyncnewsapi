import logging
import os
import sys

import aiohttp
from yarl import URL


def env_variable_api_key():
    api_key = os.environ.get('NEWSAPI_KEY')
    if not api_key:
        logger = logging.getLogger(__name__)
        logger.critical('The NEWSAPI_KEY environment variable is not set, it should contain the API key. '
                        'Go to https://newsapi.org to create a free API key.')
        sys.exit()
    return api_key


class KeyAuth(aiohttp.BasicAuth):
    '''Http API key authentication helper. Derives from BasicAuth because aiohttp checks isinstance'''

    def __new__(cls, api_key):
        if api_key is None:
            raise ValueError('None is not allowed as an API key value')
        return super().__new__(cls, login=api_key)

    @classmethod
    def from_url(cls, url, *, encoding='latin1'):
        '''Create KeyAuth from url.'''
        if not isinstance(url, URL):
            raise TypeError('url should be yarl.URL instance')
        queries = {q.split('=')[0]: q.split('=')[1] for q in url.query_string.split('&')}
        if queries.get('apiKey') is None:
            return None
        return cls(queries['apiKey'])

    @classmethod
    def decode(cls, auth_header, encoding='latin1'):
        '''Create a KeyAuth object from an Authorization HTTP header.'''
        try:
            auth_type, api_key = auth_header.split(' ', 1)
        except ValueError:
            raise ValueError('Could not parse authorization header.')
        if auth_type.lower() != 'basic':
            raise ValueError('Unknown authorization method %s' % auth_type)
        return cls(api_key)

    def encode(self):
        '''Encode credentials. NewsAPI docs specdify the key should not be base64 encoded.'''
        return self.login
