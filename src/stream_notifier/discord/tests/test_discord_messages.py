import pytest

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig

from ..messages import MultipartFormData, _get_discord_embeds, _get_image, _get_message_text
from ..schemas import DiscordEmbed, DiscordEmbedImage

EMBED_CONFIGS = [
    [DiscordEmbedConfig(
        title="Title",
        description="Description",
    )],
    [DiscordEmbedConfig(
        title="Title",
        description="Description",
        image=b"a",
    )],
    [DiscordEmbedConfig(
        title="Title",
        description="Description",
        image="https://example.com/",
    )],
    [
        DiscordEmbedConfig(
            title="Title",
            description="Description",
            image=b"a",
        ),
        DiscordEmbedConfig(
            title="Title2",
            description="Description2",
            image=b"b",
        ),
    ],
    [
        DiscordEmbedConfig(
            title="Title",
            description="Description",
            image="https://example.com/",
        ),
        DiscordEmbedConfig(
            title="Title2",
            description="Description2",
            image="https://example.com/1",
        ),
    ],
    [
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
    ],
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
        image=DiscordEmbedImage(url="attachment://embed0.png"),
    )],
    [DiscordEmbed(
        title="Title",
        description="Description",
        type="image",
        image=DiscordEmbedImage(url="https://example.com/"),
    )],
    [
        DiscordEmbed(
            title="Title",
            description="Description",
            type="image",
            image=DiscordEmbedImage(url="attachment://embed0.png"),
        ),
        DiscordEmbed(
            title="Title2",
            description="Description2",
            type="image",
            image=DiscordEmbedImage(url="attachment://embed1.png"),
        ),
    ],
    [
        DiscordEmbed(
            title="Title",
            description="Description",
            type="image",
            image=DiscordEmbedImage(url="https://example.com/"),
        ),
        DiscordEmbed(
            title="Title2",
            description="Description2",
            type="image",
            image=DiscordEmbedImage(url="https://example.com/1"),
        ),
    ],
    [
        DiscordEmbed(
            title="Title",
            description="Description",
            type="image",
            image=DiscordEmbedImage(url="attachment://embed0.png"),
        ),
        DiscordEmbed(
            title="Title",
            description="Description",
            type="image",
            image=DiscordEmbedImage(url="https://example.com/"),
        ),
    ],
]

MULTIPARTS: list[MultipartFormData] = [
    {"files[0]": ("embed0.png", b"a", "image/png")},
    {
        "files[0]": ("embed0.png", b"a", "image/png"),
        "files[1]": ("embed1.png", b"b", "image/png"),
    },
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
    "config,output_embeds,output_multipart",
    (
        ([], [], {}),
        (EMBED_CONFIGS[0], EMBEDS[0], {}),
        (EMBED_CONFIGS[1], EMBEDS[1], MULTIPARTS[0]),
        (EMBED_CONFIGS[2], EMBEDS[2], {}),
        (EMBED_CONFIGS[3], EMBEDS[3], MULTIPARTS[1]),
        (EMBED_CONFIGS[4], EMBEDS[4], {}),
        (EMBED_CONFIGS[5], EMBEDS[5], MULTIPARTS[0]),
    ),
)
def test_discord_embeds(
    config: list[DiscordEmbedConfig],
    output_embeds: list[DiscordEmbed],
    output_multipart: MultipartFormData,
) -> None:
    embeds, multipart_data = _get_discord_embeds(config)
    assert embeds == output_embeds
    assert multipart_data == output_multipart


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


@pytest.mark.parametrize(
    ("image,embeds,output"),
    (
        (None, [], None),
        (b"a", [], {"files[0]": ("image.png", b"a", "image/png")}),
        (b"a", [EMBEDS[1][0]], {"files[1]": ("image.png", b"a", "image/png")}),
        (b"a", [EMBEDS[1][0], EMBEDS[1][0], EMBEDS[0][0]], {"files[2]": ("image.png", b"a", "image/png")}),
    ),
)
def test_get_image(image: bytes | None, embeds: list[DiscordEmbed], output: MultipartFormData | None) -> None:
    assert _get_image(image, embeds) == output
