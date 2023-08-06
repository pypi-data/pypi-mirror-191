import pytest

from .admin_wells import get_all_wells, get_well, get_wells_by_registration_number
from .config import Config


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_well():
    result = get_well(1)
    assert result["WellID"] == 1


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_wells():
    results = get_all_wells()
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_wells_by_registration_number():
    result = get_wells_by_registration_number(1)
    assert len(result) >= 1
