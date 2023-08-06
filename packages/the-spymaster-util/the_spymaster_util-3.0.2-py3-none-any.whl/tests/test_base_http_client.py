from __future__ import annotations

import json
from http import HTTPStatus
from http.client import HTTPMessage
from typing import Optional
from unittest.mock import ANY, Mock, call, patch

from parameterized import parameterized
from requests import Response
from urllib3 import Retry

from the_spymaster_util.http.base_client import BaseHttpClient
from the_spymaster_util.http.defs import JSONType
from the_spymaster_util.http.errors import (
    APIError,
    BadRequestError,
    InternalServerError,
)


class CustomError(BadRequestError):
    x: int
    y: str

    @classmethod
    def create(cls, x: int, y: str) -> CustomError:
        return cls(message=f"Custom error with x={x} and y={y}", data={"x": x, "y": y})


class FakeCustomError(BadRequestError):
    @classmethod
    def get_error_code(cls) -> str:
        return "CUSTOM_ERROR"


def create_mock_response(
    status_code: int,
    payload: JSONType,
    headers: Optional[dict] = None,
) -> Response:
    response = Response()
    response.status_code = status_code
    response._content = json.dumps(payload).encode("utf-8")
    response.headers = headers or {}  # type: ignore
    return response


def create_mock_response_for_error(error: APIError) -> Response:
    return create_mock_response(status_code=error.status_code, payload=error.response_payload)


class ExampleClient(BaseHttpClient):
    def __init__(self, retry_strategy: Optional[Retry] = None):
        super().__init__(
            base_url="https://jsonplaceholder.typicode.com",
            retry_strategy=retry_strategy,
            common_errors={CustomError},
        )

    def users(self, **kwargs):
        return self.get(endpoint="users", data={}, **kwargs)

    def dummy(self):
        return self.get(endpoint="dummy", data={}, parse_response=False)


@parameterized.expand([(True,), (False,)])
def test_basic_call_parsing(with_log: bool):
    client = ExampleClient()
    data = [{"id": i} for i in range(10)]

    def new_get(*args, **kwargs):
        return create_mock_response(status_code=200, payload=data)

    with patch.object(client.session, "get", new=new_get):
        response = client.users(log_http_data=with_log)
    assert response == data


@patch("urllib3.connectionpool.HTTPConnectionPool._get_conn")
def test_retry_request(mock_get_conn):
    mock_get_conn.return_value.getresponse.side_effect = [
        Mock(status=429, msg=HTTPMessage()),  # Retry #0 (initial)
        Mock(status=429, msg=HTTPMessage()),  # Retry #1
        Mock(status=500, msg=HTTPMessage()),  # Retry #2
        Mock(status=200, msg=HTTPMessage()),  # Retry #3 (last, success)
        Mock(status=200, msg=HTTPMessage()),  # We won't get to this one.
    ]

    retry_strategy = Retry(
        total=3,
        backoff_factor=0.01,
        status_forcelist=[429, 500, 502, 503, 504],  # The HTTP response codes to retry on
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS"],  # The HTTP methods to retry on
    )
    client = ExampleClient(retry_strategy=retry_strategy)
    client.dummy()

    actual_calls = mock_get_conn.return_value.request.mock_calls
    assert actual_calls == [
        call("GET", "/dummy", body=None, headers=ANY),
        call("GET", "/dummy", body=None, headers=ANY),
        call("GET", "/dummy", body=None, headers=ANY),
        call("GET", "/dummy", body=None, headers=ANY),
    ]


@parameterized.expand(
    [
        (CustomError.create(x=1, y="a"), CustomError.create(x=1, y="a"), True),
        (
            CustomError(message="Test", http_status=HTTPStatus.BAD_REQUEST),
            CustomError(message="Test", http_status=HTTPStatus.BAD_REQUEST),
            True,
        ),
        (
            CustomError.create(x=1, y="a"),
            FakeCustomError(message="Custom error with x=1 and y=a", data={"x": 1, "y": "a"}),
            True,
        ),
        (CustomError.create(x=1, y="a"), CustomError.create(x=1, y="b"), False),
        (CustomError.create(x=1, y="a"), InternalServerError(message="a"), False),
    ]
)
def test_api_error_equality(e1: APIError, e2: APIError, equal: bool):
    if equal:
        assert e1 == e2
    else:
        assert e1 != e2


def test_api_error_get_attributes():
    error = APIError(message="Test", http_status=HTTPStatus.BAD_REQUEST, data={"x": 1, "y": "a"})
    assert error.x == error["x"] == 1
    assert error.y == error["y"] == "a"
    assert error.z is None
    assert error["z"] is None


def test_api_error_str():
    error = APIError(message="Test", http_status=HTTPStatus.BAD_REQUEST, data={"x": 1, "y": "a"})
    assert str(error) == "API_ERROR: Test"


def test_custom_exception_raised():
    """
    Test that a proper CustomError is raised when the HTTP payload contains `error_code = "CUSTOM_EXCEPTION"`.
    """
    client = ExampleClient()
    expected_error = CustomError.create(x=1, y="a")
    assert expected_error.x == 1
    assert expected_error.y == "a"
    mock_response = create_mock_response_for_error(error=expected_error)

    def new_get(*args, **kwargs):
        return mock_response

    with patch.object(client.session, "get", new=new_get):
        try:
            client.dummy()
            raise AssertionError("Expected CustomError to be raised")
        except Exception as e:
            assert expected_error == e
