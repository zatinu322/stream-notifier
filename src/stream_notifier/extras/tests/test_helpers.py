import pytest
from pydantic import HttpUrl

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig

from ..helpers import _get_discord_embeds, format_report, get_platform_configs
from ..schemas import DiscordEmbed, Notification, NotifierSettings, PlatformReport, PlatformSettings, SendReport

platform_settings = PlatformSettings(api_token="token", chat_id=1)

SETTINGS = NotifierSettings(
    discord=platform_settings,
    telegram=platform_settings,
    vk=platform_settings,
)

NOTIFICATIONS = (
    Notification(
        text="Text!",
    ),
    Notification(
        text="Text!",
        image="ID",
    ),
    Notification(
        text="Text!",
        image=b"a",
    ),
    Notification(
        text="Text!",
        image=HttpUrl("https://example.com"),
    ),
    Notification(
        embeds=[DiscordEmbed(title="Title")],
    ),
    Notification(
        embeds=[DiscordEmbed(description="Description")],
    ),
    Notification(
        text="Text!",
        embeds=[DiscordEmbed(image="ID")],
    ),
    Notification(
        embeds=[DiscordEmbed(image=b"a")],
    ),
    Notification(
        embeds=[DiscordEmbed(image=HttpUrl("https://example.com"))],
    ),
    Notification(
        image=b"a",
        embeds=[DiscordEmbed(image=b"a")],
    ),
    Notification(
        text="Text!",
        embeds=[
            DiscordEmbed(image="ID"),
            DiscordEmbed(title="Title", image=b"a"),
            DiscordEmbed(description="Description", image=HttpUrl("https://example.com")),
        ],
    ),
)

CONFIGS = (
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Text!",
        image=None,
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Text!",
        image=b"a",
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="",
        image=b"a",
        embeds=[DiscordEmbedConfig(
            title="",
            description="",
            image=b"a",
        )],
    ),
)

EMBED_CONFIGS = (
    [DiscordEmbedConfig(
        title="Title",
        description="",
        image=None,
    )],
    [DiscordEmbedConfig(
        title="",
        description="Description",
        image=None,
    )],
    [DiscordEmbedConfig(
        title="",
        description="",
        image=b"a",
    )],
    [DiscordEmbedConfig(
        title="",
        description="",
        image="https://example.com",
    )],
    [
        DiscordEmbedConfig(
            title="Title",
            description="",
            image=b"a",
        ),
        DiscordEmbedConfig(
            title="",
            description="Description",
            image="https://example.com",
        ),
    ],
)


@pytest.mark.parametrize(
    "notification,output",
    (
        (NOTIFICATIONS[0], CONFIGS[0]),
        (NOTIFICATIONS[1], CONFIGS[0]),
        (NOTIFICATIONS[2], CONFIGS[1]),
        (NOTIFICATIONS[3], CONFIGS[0]),
        (NOTIFICATIONS[9], CONFIGS[2]),

    ),
)
def test_discord_configs(notification: Notification, output: DiscordConfig) -> None:
    _, discord_config, _ = get_platform_configs(SETTINGS, notification)
    assert discord_config == output


@pytest.mark.parametrize(
    "notification,output",
    (
        (NOTIFICATIONS[4], EMBED_CONFIGS[0]),
        (NOTIFICATIONS[5], EMBED_CONFIGS[1]),
        (NOTIFICATIONS[6], []),
        (NOTIFICATIONS[7], EMBED_CONFIGS[2]),
        (NOTIFICATIONS[8], EMBED_CONFIGS[3]),
        (NOTIFICATIONS[10], EMBED_CONFIGS[4]),
    ),
)
def test_discord_embed_config(notification: Notification, output: DiscordEmbedConfig) -> None:
    assert _get_discord_embeds(notification) == output


REPORTS = (
    SendReport(
        telegram=PlatformReport(
            name="telegram",
            status="success",
        ),
        discord=PlatformReport(
            name="discord",
            status="failed",
            error_message="403 Forbidden",
        ),
        vk=PlatformReport(
            name="vk",
            status="ignored",
            error_message="Ignored",
        ),
    ),
    SendReport(
        telegram=PlatformReport(
            name="telegram",
            status="success",
        ),
        discord=PlatformReport(
            name="discord",
            status="failed",
            error_message="403 Forbidden",
        ),
        vk=PlatformReport(
            name="vk",
            status="in_progress",
        ),
    ),
)

FORMATTED_REPORTS = (
    "Отчёт об отправке уведомлений.\n\n"
    "✅ Telegram\n"
    "❌ Discord: 403 Forbidden\n"
    "⛔ Vk: Ignored\n",
    "Отчёт об отправке уведомлений.\n\n"
    "✅ Telegram\n"
    "❌ Discord: 403 Forbidden\n"
    "🔄 Vk\n",
)


@pytest.mark.parametrize(
    "report,output",
    (
        (REPORTS[0], FORMATTED_REPORTS[0]),
        (REPORTS[1], FORMATTED_REPORTS[1]),
    ),
)
def test_format_report(report: SendReport, output: str) -> None:
    assert format_report(report) == output
