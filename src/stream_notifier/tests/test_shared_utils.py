import pytest
from httpx import Request, Response

from stream_notifier.exceptions import NotifierHTTPStatusError
from stream_notifier.shared import raise_for_status

REQUEST = Request(
    url="https://example.com",
    method="GET",
)


def test_raise_for_status_200() -> None:
    response = Response(status_code=200, request=REQUEST)
    raise_for_status(response)


def test_raise_for_status_bad_code() -> None:
    response = Response(
        status_code=400,
        request=REQUEST,
    )
    with pytest.raises(NotifierHTTPStatusError):
        raise_for_status(response)
