import pytest
from pydantic import HttpUrl

from stream_notifier.shared import MultipartFormData

from ..messages import _get_image


@pytest.mark.parametrize(
    "image,output",
    (
        (None, (None, None)),
        ("image_id", ("image_id", None)),
        (HttpUrl("https://example.com"), ("https://example.com/", None)),
        (b"a", (None, {"photo": ("image.png", b"a", "image/png")})),
    ),
)
def test_get_image(
    image: str | HttpUrl | bytes | None,
    output: tuple[str | None, MultipartFormData | None],
) -> None:
    assert _get_image(image) == output
