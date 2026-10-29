from collections.abc import Awaitable, Callable

from pydantic import BaseModel

from notifier import (
    DiscordConfig,
    NotificationError,
    NotifierClient,
    NotifierHTTPStatusError,
    TelegramConfig,
    VKConfig,
)

from .schemas import PlatformReport, SendReport
from .types import Platform, Status

REQUESTS_TIMEOUT = 60


async def _send_notification(
    report: PlatformReport,
    send_coroutine: Callable[..., Awaitable[BaseModel]],
    ignored_platforms: list[Platform],
) -> None:
    if report.name in ignored_platforms:
        report.status = Status.IGNORED
        return

    try:
        response = await send_coroutine()
        report.status = Status.SUCCESS
        report.response = response.model_dump()
    except (NotifierHTTPStatusError, NotificationError) as e:
        report.status = Status.FAILED
        report.error_message = str(e)


async def send_notifications(
    discord_config: DiscordConfig | None = None,
    telegram_config: TelegramConfig | None = None,
    vk_config: VKConfig | None = None,
    ignored_platforms: list[Platform] | None = None,
) -> SendReport:
    if ignored_platforms is None:
        ignored_platforms = []

    report = SendReport(
        telegram=PlatformReport(name=Platform.TELEGRAM),
        discord=PlatformReport(name=Platform.DISCORD),
        vk=PlatformReport(name=Platform.VK),
    )

    async with NotifierClient(
        discord_config=discord_config,
        telegram_config=telegram_config,
        # vk_config=vk_config,  # TODO: Add vk support
        timeout=REQUESTS_TIMEOUT,
    ) as client:
        for platform_report, coroutine in [
            (report.telegram, client.send_telegram),
            (report.discord, client.send_discord),
            # (report.vk, client.send_vk), TODO: Add vk support
        ]:
            await _send_notification(platform_report, coroutine, ignored_platforms)

    return report
