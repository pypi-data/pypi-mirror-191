"""Access AdminPwap endpoints."""
from __future__ import annotations

import datetime as dt
from typing import Any, Optional, Union
from urllib.parse import urlencode

import pandas as pd

from .api import get_detail_view, get_paginated_list_view
from .config import Config


def _make_url(route: str) -> str:
    return Config.make_url(f"/api/v1/AdminPwap/{route}")


def _format_date(date: Union[str, dt.date]) -> str:
    if isinstance(date, dt.date):
        date = date.strftime("%Y-%m-%d")
    return date


def get_pwap_report(pwap_report_id: int) -> dict[str, Any]:
    """
    Get PWAP report by ID.

    Parameters
    ----------
    pwap_report_id : int
        The ID of the PWAP report

    Returns
    -------
    pwap_report_result : dict[str, Any]
        A PWAP report result object
    """
    return get_detail_view(
        _make_url(f"PwapReport?id={pwap_report_id}"), Config.dnr_token()
    )


def get_pwap_reports_for_range(
    start_date: Union[str, dt.date],
    end_date: Union[str, dt.date],
    all_accepted: Optional[bool] = None,
    progress_bar: bool = True,
) -> pd.DataFrame:
    """
    Get all PWAP reports for a date range.

    Parameters
    ----------
    start_date : str | dt.date
        The start date string in YY-mm-dd format or a date object
    end_date : str | dt.date
        The end date string in YY-mm-dd format or a date object
    all_accepted : bool
        Whether to return only accepted reports
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    pwap_reports_df : pd.DataFrame
        A DataFrame with PWAP reports records
    """
    url_params = {
        "startDate": _format_date(start_date),
        "endDate": _format_date(end_date),
        "page": 1,
    }
    if all_accepted is not None:
        url_params["allAccepted"] = "true" if all_accepted else "false"
    route = f"PwapReportsForRange?{urlencode(url_params)}"
    return get_paginated_list_view(_make_url(route), progress_bar, Config.dnr_token())


def get_pwap_gis_stream_reaches_accepted(
    since_date: Optional[Union[str, dt.date]] = None,
    days_ago: Optional[int] = None,
    progress_bar: bool = True,
) -> pd.DataFrame:
    """
    Get all PWAP GIS stream reaches accepted by sinceDate or daysAgo.

    Parameters
    ----------
    since_date : str | dt.date, optional
        The since date string in YY-mm-dd format or a date object
    days_ago : int, optional
        Filter results by days ago
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    pwap_gis_stream_reaches_df : pd.DataFrame
        A DataFrame with PWAP GIS stream reach records
    """
    url_params = {"page": 1}
    if since_date is not None:
        url_params["sinceDate"] = _format_date(since_date)
    if days_ago is not None:
        url_params["daysAgo"] = days_ago
    route = f"PwapGisStreamReachesAccepted?{urlencode(url_params)}"
    return get_paginated_list_view(_make_url(route), progress_bar, Config.dnr_token())


def get_pwap_gis_stream_reaches_latest(
    since_date: Optional[Union[str, dt.date]] = None,
    days_ago: Optional[int] = None,
    progress_bar: bool = True,
) -> pd.DataFrame:
    """
    Get latest PWAP GIS stream reaches by sinceDate or daysAgo.

    Parameters
    ----------
    since_date : str | dt.date, optional
        The since date string in YY-mm-dd format or a date object
    days_ago : int, optional
        Filter results by days ago
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    pwap_gis_stream_reaches_df : pd.DataFrame
        A DataFrame with PWAP GIS stream reach records
    """
    url_params = {"page": 1}
    if since_date is not None:
        url_params["sinceDate"] = _format_date(since_date)
    if days_ago is not None:
        url_params["daysAgo"] = days_ago
    route = f"PwapGisStreamReachesLatest?{urlencode(url_params)}"
    return get_paginated_list_view(_make_url(route), progress_bar, Config.dnr_token())


def get_pwap_gis_target_flows_accepted(
    since_date: Optional[Union[str, dt.date]] = None,
    days_ago: Optional[int] = None,
    progress_bar: bool = True,
) -> pd.DataFrame:
    """
    Get all PWAP GIS target flows accepted by sinceDate or daysAgo.

    Parameters
    ----------
    since_date : str | dt.date, optional
        The since date string in YY-mm-dd format or a date object
    days_ago : int, optional
        Filter results by days ago
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    pwap_gis_target_flows_df : pd.DataFrame
        A DataFrame with PWAP GIS target flow records
    """
    url_params = {"page": 1}
    if since_date is not None:
        url_params["sinceDate"] = _format_date(since_date)
    if days_ago is not None:
        url_params["daysAgo"] = days_ago
    route = f"PwapGisTargetFlowsAccepted?{urlencode(url_params)}"
    return get_paginated_list_view(_make_url(route), progress_bar, Config.dnr_token())


def get_pwap_gis_target_flows_latest(
    since_date: Optional[Union[str, dt.date]] = None,
    days_ago: Optional[int] = None,
    progress_bar: bool = True,
) -> pd.DataFrame:
    """
    Get latest PWAP GIS target flows by sinceDate or daysAgo.

    Parameters
    ----------
    since_date : str | dt.date, optional
        The since date string in YY-mm-dd format or a date object
    days_ago : int, optional
        Filter results by days ago
    progress_bar : bool
        Whether to display a progress bar (defaults to True)

    Returns
    -------
    pwap_gis_target_flows_df : pd.DataFrame
        A DataFrame with PWAP GIS target flow records
    """
    url_params = {"page": 1}
    if since_date is not None:
        url_params["sinceDate"] = _format_date(since_date)
    if days_ago is not None:
        url_params["daysAgo"] = days_ago
    route = f"PwapGisTargetFlowsLatest?{urlencode(url_params)}"
    return get_paginated_list_view(_make_url(route), progress_bar, Config.dnr_token())
