import pytest

from .config import Config
from .water_rights import (
    get_all_surface_water_boundaries,
    get_all_surface_water_points,
    get_surface_water_boundary,
    get_surface_water_points,
)


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_surface_water_points():
    result = get_surface_water_points(1)
    assert result["RightID"] == 1


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_surface_water_points():
    results = get_all_surface_water_points()
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_surface_water_boundary():
    result = get_surface_water_boundary(1)
    assert result["RightID"] == 1


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_surface_water_boundaries():
    results = get_all_surface_water_boundaries()
    assert len(results) >= 150
