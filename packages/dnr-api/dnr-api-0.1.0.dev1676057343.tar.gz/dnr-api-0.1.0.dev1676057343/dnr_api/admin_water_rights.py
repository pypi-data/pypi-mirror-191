"""Access AdminWaterRights endpoints."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .api import get_detail_view, get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/AdminWaterRights/{route}")


def get_surface_water_points(right_id: int) -> dict[str, Any]:
    """
    Get surface water points by Right ID.

    Parameters
    ----------
    right_id : int
        The ID of the water right

    Returns
    -------
    surface_water_points_result : dict[str, Any]
        A surface water points result object
    """
    return get_detail_view(
        _make_url(f"SurfaceWaterPoints?rightId={right_id}"), Config.dnr_token()
    )


def get_all_surface_water_points(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all available surface water points.

    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    surface_water_points_df : pd.DataFrame
        A DataFrame with surface water points records
    """
    return get_paginated_list_view(
        _make_url("AllSurfaceWaterPoints?page=1"), progress_bar, Config.dnr_token()
    )


def get_surface_water_boundary(right_id: int) -> dict[str, Any]:
    """
    Get surface water boundary by Right ID.

    Parameters
    ----------
    right_id : int
        The ID of the water right

    Returns
    -------
    surface_water_boundary_result : dict[str, Any]
        A surface water boundary result object
    """
    return get_detail_view(
        _make_url(f"SurfaceWaterBoundary?rightId={right_id}"), Config.dnr_token()
    )


def get_all_surface_water_boundaries(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all available surface water boundaries.

    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    surface_water_boundaries_df : pd.DataFrame
        A DataFrame with surface water boundary records
    """
    return get_paginated_list_view(
        _make_url("AllSurfaceWaterBoundaries?page=1"), progress_bar, Config.dnr_token()
    )
