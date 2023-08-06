import pytest

from .admin_floodplain import get_all_floodplain_lomcs, get_all_nebraska_sections
from .config import Config


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_nebraska_sections():
    results = get_all_nebraska_sections()
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_floodplain_lomcs():
    results = get_all_floodplain_lomcs()
    assert len(results) >= 150
