from http.client import HTTPException
from unittest.mock import patch

from wait_for.http import http, https


@patch("http.client.HTTPConnection.request")
def test_http_failed(mock_http_request):
    mock_http_request.side_effect = HTTPException("error")

    assert (
        http(
            address="www.unreachable.com",
            url="/",
            method="GET",
            timeout=None,
            validate_status=lambda status: status == 200,
        )
        is False
    )


@patch("http.client.HTTPConnection.getresponse")
@patch("http.client.HTTPConnection.request")
def test_http_success(mock_http_request, mock_http_getresponse):
    mock_http_request.return_value = None
    mock_http_getresponse.return_value.status = 200

    assert http(
        address="google.com",
        url="/",
        method="GET",
        timeout=None,
        validate_status=lambda status: True,
    )


@patch("http.client.HTTPConnection.getresponse")
@patch("http.client.HTTPConnection.request")
def test_https_success(mock_http_request, mock_http_getresponse):
    mock_http_request.return_value = None
    mock_http_getresponse.return_value.status = 200

    assert https(
        address="google.com",
        url="/",
        method="GET",
        timeout=None,
        validate_status=lambda status: True,
    )
