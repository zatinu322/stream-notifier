from httpx import HTTPStatusError, Response
from pydantic import ConfigDict

from .exceptions import NotifierHTTPStatusError

request_model_config = ConfigDict(
    extra="forbid",
    validate_default=True,
)

response_model_config = ConfigDict(
    extra="ignore",
    populate_by_name=True,
)


def raise_for_status(response: Response) -> None:
    "Check whether response has 2xx status code and raise exception otherwise."
    try:
        response.raise_for_status()
    except HTTPStatusError:
        raise NotifierHTTPStatusError(
            response=response,
            message="HTTP status error.",
        )
