from pathlib import Path

import pytest
from pydantic import HttpUrl, ValidationError

from ..schemas import Notification


def test_no_images() -> None:
    notification = Notification(image=None, embed_image=None)
    assert notification.image is None
    assert notification.embed_image is None


def test_image_id() -> None:
    notification = Notification(image="ID", embed_image="ID")
    assert notification.image == "ID"
    assert notification.embed_image == "ID"


def test_invalid_image() -> None:
    with pytest.raises(ValidationError):
        Notification(image=1)

    with pytest.raises(ValidationError):
        Notification(embed_image=1)


def test_image_url() -> None:
    notification = Notification(
        image="https://example.com/image.png",
        embed_image="http://example.com/image.png",
    )

    assert notification.image == HttpUrl("https://example.com/image.png")
    assert notification.embed_image == HttpUrl("http://example.com/image.png")


def test_image_bytes() -> None:
    image_path = str(Path(__file__).parent / "test")
    notification = Notification(image=image_path, embed_image=image_path)
    assert notification.image == b"a\n"
    assert notification.embed_image == b"a\n"
