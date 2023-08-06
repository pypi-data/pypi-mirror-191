"""Access AdminWells endpoints."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .api import get_detail_view, get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/AdminWells/{route}")


def get_well(well_id: int) -> dict[str, Any]:
    """
    Get well information by a Well ID.

    Parameters
    ----------
    well_id : int
        The ID well

    Returns
    -------
    well_result : dict[str, Any]
        A well result object
    """
    return get_detail_view(_make_url(f"Well?id={well_id}"), Config.dnr_token())


def get_wells_by_registration_number(
    registration_number: str, progress_bar: bool = True
) -> pd.DataFrame:
    """
    Get all wells for a registration number.

    Parameters
    ----------
    registration_number : str
        The registration number for the wells
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    wells_df : pd.DataFrame
        A DataFrame with well records
    """
    route = f"WellsByRegistrationNumber?RegistrationNumber={registration_number}&page=1"
    return get_paginated_list_view(_make_url(route), progress_bar, Config.dnr_token())


def get_all_wells(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all available wells.

    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    wells_df : pd.DataFrame
        A DataFrame with well records
    """
    return get_paginated_list_view(
        _make_url("AllWells?page=1"), progress_bar, Config.dnr_token()
    )
