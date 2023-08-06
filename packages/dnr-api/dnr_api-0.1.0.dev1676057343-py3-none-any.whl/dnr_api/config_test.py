import os
from unittest import mock

import pytest

from .config import Config


def test_make_url__strips_leading_slash():
    url = Config.make_url("/foobar")
    assert url == f"{Config.base_url}/foobar"


def test_dnr_token__raises_when_not_set():
    with mock.patch.dict(os.environ, {}, clear=True), pytest.raises(ValueError):
        Config.dnr_token()


def test_dnr_token__returns_dnr_token_env_variable():
    dnr_token = "foo bar"
    with mock.patch.dict(os.environ, {"DNR_TOKEN": dnr_token}):
        assert Config.dnr_token() == dnr_token
