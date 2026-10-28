import pytest
from pydantic import ValidationError

from ..config import DiscordConfig, DiscordEmbedConfig

EMBED_CONFIG = DiscordEmbedConfig(title="test", description="test")


def test_discord_message_content_missing() -> None:
    with pytest.raises(ValidationError):
        DiscordConfig(
            api_token="token",
            channel_id=1,
        )


@pytest.mark.parametrize(
    "text,image,embed_config",
    (
        ("text", None, None),
        ("", b"a", None),
        ("", None, EMBED_CONFIG),
        ("text", b"a", None),
        ("text", None, EMBED_CONFIG),
        ("", b"a", EMBED_CONFIG),
        ("text", b"a", EMBED_CONFIG),
    ),
)
def test_discord_message_content_ok(text: str, image: bytes | None, embed_config: DiscordEmbedConfig | None) -> None:
    assert DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text=text,
        image=image,
        embed=embed_config,
    )
