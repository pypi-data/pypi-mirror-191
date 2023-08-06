from __future__ import annotations

import sys
import warnings
from typing import Any, Optional, Union

import pandas as pd
import requests
from tqdm import tqdm

from .config import Config


class APIError(Exception):
    """An error accessing the DNR API"""

    pass


class APIResponse:
    def __init__(self, response: requests.Response) -> None:
        response.raise_for_status()
        self.parsed_response: dict[str, Any] = response.json()

    @property
    def links(self) -> dict[str, Any]:
        links = self.parsed_response.get("Links")
        if not isinstance(links, dict):
            raise APIError(f"Invalid 'Links' attribute: {links}.")
        return links

    @property
    def total_records(self) -> int:
        total_records = self.links.get("TotalRecords")
        if total_records is None:
            warnings.warn(
                f"'TotalRecords' is missing from response. "
                "Will continue requesting pages until 'NextPageUrl' is null."
            )
        elif not isinstance(total_records, int):
            raise APIError(f"Invalid 'TotalRecords' attribute: {total_records}")
        return total_records

    @property
    def next_page_url(self) -> Union[str, None]:
        next_page_url = self.links.get("NextPageUrl")
        if not isinstance(next_page_url, str) and next_page_url is not None:
            raise APIError(f"Invalid 'NextPageUrl' attribute: {next_page_url}")
        return next_page_url

    @property
    def results(self) -> list[dict[str, Any]]:
        """A list of results in the response."""
        results = self.parsed_response.get("Results")
        if not isinstance(results, list):
            raise APIError(f"Invalid 'Results' attribute: {results}")
        return results

    @property
    def result(self) -> dict[str, Any]:
        """A single result object in the response."""
        result = self.parsed_response.get("Result")
        if not isinstance(result, dict):
            raise APIError(f"Invalid 'Result' attribute: {result}")
        return result


def get_paginated_list_view(
    url: str,
    progress_bar: bool = True,
    admin_token: Optional[str] = None,
) -> pd.DataFrame:
    """Get a paginated list of results and return a DataFrame."""
    headers: dict[str, str] = {}
    if admin_token:
        headers["Authorization"] = admin_token
    # Truncate results for API tests
    n_records = sys.maxsize
    if Config.api_test():
        n_records = 150
    response = APIResponse(requests.get(url, headers=headers))
    records = list(response.results)
    if progress_bar:
        pbar = tqdm(total=response.total_records)
        pbar.update(len(response.results))
    while response.next_page_url and len(records) < n_records:
        response = APIResponse(requests.get(response.next_page_url, headers=headers))
        records.extend(response.results)
        if progress_bar:
            pbar.update(len(response.results))
    return pd.DataFrame(records)


def get_detail_view(url: str, admin_token: Optional[str] = None) -> dict[str, Any]:
    """Get a detail view of an object."""
    headers: dict[str, str] = {}
    if admin_token:
        headers["Authorization"] = admin_token
    response = APIResponse(requests.get(url, headers=headers))
    return response.result
