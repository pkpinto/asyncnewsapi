import os
import pytest
import sys

from asyncnewsapi.auth import env_variable_api_key


def test_env_variable_api_key(monkeypatch):
    monkeypatch.delenv('NEWSAPI_KEY', raising=False)
    with pytest.raises(SystemExit):
        env_variable_api_key()
