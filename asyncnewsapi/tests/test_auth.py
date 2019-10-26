import os
import sys

import pytest
from yarl import URL

from asyncnewsapi.auth import env_variable_api_key, KeyAuth


def test_env_variable_api_key(monkeypatch):
    monkeypatch.delenv('NEWSAPI_KEY', raising=False)
    with pytest.raises(SystemExit):
        env_variable_api_key()


class TestAuth(object):

    def test_keyauth_from_url(self):
        keyauth = KeyAuth(api_key='test_api_key')
        assert(keyauth.from_url(URL('https://newsapi.org/v2/top-headlines?email=john@email.com&apiKey=test_api_key')) == keyauth)

    def test_keyauth_decode(self):
        assert(KeyAuth.decode('Basic test_api_key').encode() == 'test_api_key')

    def test_keyauth_encode(self):
        keyauth = KeyAuth(api_key='test_api_key')
        assert(keyauth.encode() == 'test_api_key')
