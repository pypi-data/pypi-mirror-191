import pytest
import requests
from requests_mock import Mocker

from .api import APIError, APIResponse, get_detail_view, get_paginated_list_view

FAKE_URL = "https://foobar.com"
FAKE_URL2 = "https://helloworld.com"
DUMMY_OBJECT = {"foo": "bar"}
LINKS_OBJECT = {"TotalRecords": 100, "NextPageUrl": FAKE_URL}
RESULTS_LIST = [DUMMY_OBJECT]
AUTH_TOKEN = "hello world!"
HEADER_OBJECT = {"Authorization": AUTH_TOKEN}


def test_api_response__raises_for_status(requests_mock: Mocker):
    requests_mock.register_uri("GET", FAKE_URL, status_code=401)
    with pytest.raises(requests.HTTPError):
        APIResponse(requests.get(FAKE_URL))


def test_api_response__parses_json(requests_mock: Mocker):
    requests_mock.get(FAKE_URL, json=DUMMY_OBJECT)
    response = APIResponse(requests.get(FAKE_URL))
    assert response.parsed_response == DUMMY_OBJECT


def test_api_response__parses_links_object(requests_mock: Mocker):
    valid_body = {"Links": LINKS_OBJECT, **DUMMY_OBJECT}
    requests_mock.get(FAKE_URL, json=valid_body)
    response = APIResponse(requests.get(FAKE_URL))
    assert response.links == LINKS_OBJECT

    invalid_body = DUMMY_OBJECT
    requests_mock.get(FAKE_URL, json=invalid_body)
    response = APIResponse(requests.get(FAKE_URL))
    with pytest.raises(APIError):
        response.links


def test_api_response__parses_total_records(requests_mock: Mocker):
    valid_body = {"Links": LINKS_OBJECT}
    requests_mock.get(FAKE_URL, json=valid_body)
    response = APIResponse(requests.get(FAKE_URL))
    assert response.total_records == LINKS_OBJECT["TotalRecords"]

    warning_body = {"Links": {**LINKS_OBJECT, "TotalRecords": None}}
    requests_mock.get(FAKE_URL, json=warning_body)
    response = APIResponse(requests.get(FAKE_URL))
    with pytest.warns(UserWarning):
        assert response.total_records is None

    invalid_body = {"Links": {**LINKS_OBJECT, "TotalRecords": "Bad value"}}
    requests_mock.get(FAKE_URL, json=invalid_body)
    response = APIResponse(requests.get(FAKE_URL))
    with pytest.raises(APIError):
        response.total_records


def test_api_response__parses_next_page_url(requests_mock: Mocker):
    valid_body = {"Links": LINKS_OBJECT}
    requests_mock.get(FAKE_URL, json=valid_body)
    response = APIResponse(requests.get(FAKE_URL))
    assert response.next_page_url == FAKE_URL

    valid_body = {"Links": {**LINKS_OBJECT, "NextPageUrl": None}}
    requests_mock.get(FAKE_URL, json=valid_body)
    response = APIResponse(requests.get(FAKE_URL))
    assert response.next_page_url is None

    invalid_body = {"Links": {**LINKS_OBJECT, "NextPageUrl": 500}}
    requests_mock.get(FAKE_URL, json=invalid_body)
    response = APIResponse(requests.get(FAKE_URL))
    with pytest.raises(APIError):
        response.next_page_url


def test_api_response__parses_results_list(requests_mock: Mocker):
    valid_body = {"Results": RESULTS_LIST}
    requests_mock.get(FAKE_URL, json=valid_body)
    response = APIResponse(requests.get(FAKE_URL))
    assert len(response.results) == len(RESULTS_LIST)

    invalid_body = {"Results": DUMMY_OBJECT}
    requests_mock.get(FAKE_URL, json=invalid_body)
    response = APIResponse(requests.get(FAKE_URL))
    with pytest.raises(APIError):
        response.results


def test_api_response__parses_single_result(requests_mock: Mocker):
    valid_body = {"Result": DUMMY_OBJECT}
    requests_mock.get(FAKE_URL, json=valid_body)
    response = APIResponse(requests.get(FAKE_URL))
    assert response.result == DUMMY_OBJECT

    invalid_body = {"Result": RESULTS_LIST}
    requests_mock.get(FAKE_URL, json=invalid_body)
    response = APIResponse(requests.get(FAKE_URL))
    with pytest.raises(APIError):
        response.result


def test_get_detail_view__returns_results_list(requests_mock: Mocker):
    valid_body1 = {
        "Links": {"TotalRecords": 1, "NextPageUrl": FAKE_URL2},
        "Results": RESULTS_LIST,
    }
    valid_body2 = {"Links": {"TotalRecords": 1}, "Results": RESULTS_LIST}
    requests_mock.get(FAKE_URL, json=valid_body1)
    requests_mock.get(FAKE_URL2, json=valid_body2)
    assert len(get_paginated_list_view(FAKE_URL, admin_token=AUTH_TOKEN)) == 2


def test_get_detail_view__returns_single_result(requests_mock: Mocker):
    valid_body = {"Result": DUMMY_OBJECT}
    requests_mock.get(FAKE_URL, json=valid_body)
    assert get_detail_view(FAKE_URL) == DUMMY_OBJECT

    # Make sure we're correctly passing auth tokens
    requests_mock.get(FAKE_URL2, json=valid_body, request_headers=HEADER_OBJECT)
    assert get_detail_view(FAKE_URL2, AUTH_TOKEN) == DUMMY_OBJECT
