"""Access AdminWaterUse endpoints."""
import pandas as pd

from .api import get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/AdminWaterUse/{route}")


def get_water_use_by_year(year: int, progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all completed water use records for a given year.

    Parameters
    ----------
    year : int
        The year for which to get water use records
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    water_use_df : pd.DataFrame
        A DataFrame with water use records
    """
    return get_paginated_list_view(
        _make_url(f"CompletedWaterUseByYear?year={year}&page=1"),
        progress_bar,
        Config.dnr_token(),
    )
