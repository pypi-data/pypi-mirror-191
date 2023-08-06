import pytest

from .admin_water_use import get_water_use_by_year
from .config import Config


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_water_use_by_year():
    results = get_water_use_by_year(2022)
    assert len(results) >= 150
