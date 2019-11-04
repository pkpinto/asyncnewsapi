import os
import sys

import pytest
from yarl import URL

from asyncnewsapi.auth import env_variable_api_key, KeyAuth


def test_env_variable_api_key(monkeypatch):
    monkeypatch.delenv('NEWSAPI_KEY', raising=False)
    with pytest.raises(SystemExit):
        env_variable_api_key()


class TestAuth:

    def test_api_key_not_none(self):
        with pytest.raises(ValueError):
            KeyAuth(None)

    def test_from_url(self):
        assert(KeyAuth.from_url(URL('https://newsapi.org/v2/top-headlines?email=john@email.com&apiKey=test_api_key')) == KeyAuth(api_key='test_api_key'))

    def test_from_url_uses_yarl(self):
        '''from_url takes url as a yarnl.URL object'''
        with pytest.raises(TypeError):
            KeyAuth.from_url('https://newsapi.org/v2/top-headlines?email=john@email.com&apiKey=test_api_key')

    def test_from_url_no_api_key(self):
        assert(KeyAuth.from_url(URL('https://newsapi.org/v2/top-headlines?email=john@email.com')) is None)

    def test_decode(self):
        assert(KeyAuth.decode('Basic test_api_key').encode() == 'test_api_key')

    def test_decode_cannot_parse(self):
        '''Authorization HTTP header should look like "Basic test_api_key"'''
        with pytest.raises(ValueError):
            KeyAuth.decode('test_api_key')

    def test_decode_not_basic_auth(self):
        '''Authorization HTTP header should look like "Basic test_api_key"'''
        with pytest.raises(ValueError):
            KeyAuth.decode('Not basic test_api_key')

    def test_encode(self):
        keyauth = KeyAuth(api_key='test_api_key')
        assert(keyauth.encode() == 'test_api_key')
