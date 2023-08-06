"""Access Dams endpoints."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .api import get_detail_view, get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/Dams/{route}")


def get_dam(dam_id: int) -> dict[str, Any]:
    """
    Get dam information by Dam ID.
    
    Parameters
    ----------
    dam_id : int
        The ID of the dam

    Returns
    -------
    dam_result : dict[str, Any]
        A dam result object
    """
    return get_detail_view(_make_url(f"Dam?id={dam_id}"))


def get_all_dams(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all available public dams.
    
    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    dams_df : pd.DataFrame
        A DataFrame with dam records
    """
    return get_paginated_list_view(_make_url("AllDams?page=1"), progress_bar)
