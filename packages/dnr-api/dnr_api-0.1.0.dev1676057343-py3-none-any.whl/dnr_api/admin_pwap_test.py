import datetime as dt

import pytest

from .admin_pwap import (
    get_pwap_gis_stream_reaches_accepted,
    get_pwap_gis_stream_reaches_latest,
    get_pwap_gis_target_flows_accepted,
    get_pwap_gis_target_flows_latest,
    get_pwap_report,
    get_pwap_reports_for_range,
)
from .config import Config


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_pwap_report():
    result = get_pwap_report(2826)
    assert result["PwapReportId"] == 2826


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_pwap_reports_for_range():
    results = get_pwap_reports_for_range(
        dt.date(2022, 1, 1), dt.date(2023, 1, 1), all_accepted=False
    )
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_pwap_gis_stream_reaches_accepted():
    results = get_pwap_gis_stream_reaches_accepted(dt.date(2022, 1, 1), 1000)
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_pwap_gis_stream_reaches_latest():
    results = get_pwap_gis_stream_reaches_latest(dt.date(2022, 1, 1), 1000)
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_pwap_gis_target_flows_accepted():
    results = get_pwap_gis_target_flows_accepted(dt.date(2022, 1, 1), 1000)
    assert len(results) >= 150


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_pwap_gis_target_flows_latest():
    results = get_pwap_gis_target_flows_latest(dt.date(2022, 1, 1), 1000)
    assert len(results) >= 150
