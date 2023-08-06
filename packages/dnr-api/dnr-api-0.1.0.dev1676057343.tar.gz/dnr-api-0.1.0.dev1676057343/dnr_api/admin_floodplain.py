"""Access AdminFloodplain endpoints."""
from __future__ import annotations

import pandas as pd

from .api import get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/AdminFloodplain/{route}")


def get_all_nebraska_sections(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all Nebraska sections.

    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    nebraska_sections_df : pd.DataFrame
        A DataFrame with Nebraska sections records
    """
    return get_paginated_list_view(
        _make_url(f"AllNebraskaSections?page=1"), progress_bar, Config.dnr_token()
    )


def get_all_floodplain_lomcs(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all Floodplain LOMCs.

    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    floodplain_lomcs_df : pd.DataFrame
        A DataFrame with Floodplain LOMC records
    """
    return get_paginated_list_view(
        _make_url(f"AllFloodplainLOMCs?page=1"), progress_bar, Config.dnr_token()
    )
