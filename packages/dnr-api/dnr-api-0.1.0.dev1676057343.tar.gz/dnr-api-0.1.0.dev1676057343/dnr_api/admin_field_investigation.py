"""Access AdminFieldInvestigation endpoints."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .api import get_detail_view, get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/AdminFieldInvestigation/{route}")


def get_field_investigation_report(
    field_investigation_report_id: int,
) -> dict[str, Any]:
    """
    Get field investigation report by Field Investigation Report ID.
    
    Parameters
    ----------
    field_investigation_report_id : int
        The ID of the field investigation report

    Returns
    -------
    field_investigation_report_result : dict[str, Any]
        A field investigation report result object
    """
    route = f"FieldInvestigationReport?FieldInvestigationReportId={field_investigation_report_id}"
    return get_detail_view(_make_url(route), Config.dnr_token())


def get_all_field_investigations(progress_bar: bool = True) -> pd.DataFrame:
    """
    Get all available field investigation reports.
    
    Parameters
    ----------
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    field_investigations_df : pd.DataFrame
        A DataFrame with field investigation records
    """
    return get_paginated_list_view(
        _make_url("AllFieldInvestigations?page=1"), progress_bar, Config.dnr_token()
    )
