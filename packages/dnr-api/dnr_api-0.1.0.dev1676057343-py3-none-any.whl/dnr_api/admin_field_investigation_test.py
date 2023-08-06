import pytest

from .admin_field_investigation import (
    get_all_field_investigations,
    get_field_investigation_report,
)
from .config import Config


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_field_investigation_report():
    result = get_field_investigation_report(164)
    assert result["FieldInvestigationReportID"] == 164


@pytest.mark.skipif(not Config.api_test(), reason="api")
def test_get_all_field_investigations():
    results = get_all_field_investigations()
    assert len(results) >= 150
