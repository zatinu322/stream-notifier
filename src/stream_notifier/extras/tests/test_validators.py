from pathlib import Path

import pytest
from pydantic import HttpUrl, ValidationError

from ..schemas import DiscordEmbed, Notification

IMAGE_PATH = str(Path(__file__).parent / "test")


@pytest.mark.parametrize(
    "image,embed_image,validated_image,validated_embed_image",
    (
        (None, None, None, None),
        ("ID", "ID", "ID", "ID"),
        (
            "https://example.com/image.png",
            "https://example.com/image.png",
            HttpUrl("https://example.com/image.png"),
            HttpUrl("https://example.com/image.png"),
        ),
        (IMAGE_PATH, IMAGE_PATH, b"a\n", b"a\n"),
    ),
)
def test_image_validation_ok(
    image: str | None,
    embed_image: str | None,
    validated_image: str | HttpUrl | bytes | None,
    validated_embed_image: str | HttpUrl | bytes | None,
) -> None:
    notification = Notification(
        image=image,
        embeds=[DiscordEmbed(
            image=embed_image,
        )],
    )
    assert notification.image == validated_image
    assert notification.embeds[0].image == validated_embed_image


def test_invalid_image() -> None:
    with pytest.raises(ValidationError):
        Notification(image=1)

    with pytest.raises(ValidationError):
        Notification(embeds=[DiscordEmbed(image=1)])
