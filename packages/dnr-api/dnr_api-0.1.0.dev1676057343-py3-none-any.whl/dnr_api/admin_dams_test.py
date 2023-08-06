import pytest

from .admin_dams import get_all_dams, get_dam
from .config import Config


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_dam():
    result = get_dam(1)
    assert result["DamID"] == 1


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_dams():
    results = get_all_dams()
    assert len(results) >= 150
