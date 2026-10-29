import pytest

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig

from ..messages import MultipartFormData, _get_discord_embeds, _get_message_text
from ..schemas import DiscordEmbed, DiscordEmbedImage

EMBED_CONFIGS = [
    DiscordEmbedConfig(
        title="Title",
        description="Description",
    ),
    DiscordEmbedConfig(
        title="Title",
        description="Description",
        image=b"a",
    ),
    DiscordEmbedConfig(
        title="Title",
        description="Description",
        image="https://example.com/",
    ),
]

EMBEDS = [
    [DiscordEmbed(
        title="Title",
        description="Description",
        type="rich",
    )],
    [DiscordEmbed(
        title="Title",
        description="Description",
        type="image",
        image=DiscordEmbedImage(url="attachment://embed.png"),
    )],
    [DiscordEmbed(
        title="Title",
        description="Description",
        type="image",
        image=DiscordEmbedImage(url="https://example.com/"),
    )],
]

MULTIPARTS: list[tuple[MultipartFormData, ...]] = [
    (
        {
            "a": ("b", b"c", "d"),
        },
        {
            "a": ("b", b"c", "d"),
            "files[0]": ("embed.png", b"a", "image/png"),
        },
    ),
    ({"a": ("b", b"c", "d")}, {"a": ("b", b"c", "d")}),
]

CONFIGS = [
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Test",
        users_to_mention=[],
        roles_to_mention=[],
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Test",
        users_to_mention=["1", "2"],
        roles_to_mention=[],
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Test",
        users_to_mention=[],
        roles_to_mention=["3", "4"],
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Test",
        users_to_mention=["1", "2"],
        roles_to_mention=["3", "4"],
    ),
]

TEXT_OUTPUTS = [
    "Test",
    "<@1> <@2>\nTest",
    "<@&3> <@&4>\nTest",
    "<@1> <@2> <@&3> <@&4>\nTest",
]


@pytest.mark.parametrize(
    "config,multipart,output,mutated_multipart",
    (
        (None, {}, [], {}),
        (EMBED_CONFIGS[0], {}, EMBEDS[0], {}),
        (EMBED_CONFIGS[1], MULTIPARTS[0][0], EMBEDS[1], MULTIPARTS[0][1]),
        (EMBED_CONFIGS[2], MULTIPARTS[1][0], EMBEDS[2], MULTIPARTS[1][1]),
    ),
)
def test_discord_embeds(
    config: DiscordEmbedConfig | None,
    multipart: MultipartFormData,
    output: list[DiscordEmbed],
    mutated_multipart: MultipartFormData,
) -> None:
    assert _get_discord_embeds(config, multipart) == output
    assert multipart == mutated_multipart


@pytest.mark.parametrize(
    "discord_config,output",
    (
        (CONFIGS[0], TEXT_OUTPUTS[0]),
        (CONFIGS[1], TEXT_OUTPUTS[1]),
        (CONFIGS[2], TEXT_OUTPUTS[2]),
        (CONFIGS[3], TEXT_OUTPUTS[3]),
    ),
)
def test_discord_message_text(discord_config: DiscordConfig, output: str) -> None:
    assert _get_message_text(discord_config) == output
