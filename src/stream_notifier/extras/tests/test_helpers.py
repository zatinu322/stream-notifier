import pytest
from pydantic import HttpUrl

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig

from ..helpers import _get_discord_embed, format_report, get_platform_configs
from ..schemas import Notification, NotifierSettings, PlatformReport, PlatformSettings, SendReport

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
        embed_title="Title",
    ),
    Notification(
        embed_description="Description",
    ),
    Notification(
        text="Text!",
        embed_image="ID",
    ),
    Notification(
        embed_image=b"a",
    ),
    Notification(
        embed_image=HttpUrl("https://example.com"),
    ),
    Notification(
        image=b"a",
        embed_image=b"a",
    ),
)

CONFIGS = (
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Text!",
        image=None,
        embed=None,
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="Text!",
        image=b"a",
        embed=None,
    ),
    DiscordConfig(
        api_token="token",
        channel_id=1,
        message_text="",
        image=b"a",
        embed=DiscordEmbedConfig(
            title="",
            description="",
            image=b"a",
        ),
    ),
)

EMBED_CONFIGS = (
    DiscordEmbedConfig(
        title="Title",
        description="",
        image=None,
    ),
    DiscordEmbedConfig(
        title="",
        description="Description",
        image=None,
    ),
    DiscordEmbedConfig(
        title="",
        description="",
        image=b"a",
    ),
    DiscordEmbedConfig(
        title="",
        description="",
        image="https://example.com",
    ),
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
        (NOTIFICATIONS[6], None),
        (NOTIFICATIONS[7], EMBED_CONFIGS[2]),
        (NOTIFICATIONS[8], EMBED_CONFIGS[3]),
    ),
)
def test_discord_embed_config(notification: Notification, output: DiscordEmbedConfig) -> None:
    assert _get_discord_embed(notification) == output


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
    "⛔ Vk\n",
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
