import yaml
from pydantic import HttpUrl

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig, TelegramConfig, VKConfig

from .schemas import Notification, NotifierSettings, SendReport
from .types import Status

REPORT_TEMPLATE = """Отчёт об отправке уведомлений.

{report}
"""

EMOJI_TO_STATUS = {
    Status.SUCCESS: "✅",
    Status.FAILED: "❌",
    Status.IGNORED: "⛔",
    Status.IN_PROGRESS: "🔄",
}


def load_notification_from_yaml(notification_path: str) -> Notification:
    with open(notification_path, encoding="utf-8") as stream:
        notification = yaml.safe_load(stream)
    return Notification.model_validate(notification)


def _get_discord_embed(notification: Notification) -> DiscordEmbedConfig | None:
    title = notification.embed_title
    description = notification.embed_description
    image = notification.embed_image if isinstance(notification.embed_image, (HttpUrl, bytes)) else None

    if not (title or description or image):
        return None

    return DiscordEmbedConfig(
        title=notification.embed_title,
        description=notification.embed_description,
        image=image,
    )


def get_platform_configs(
    settings: NotifierSettings,
    notification: Notification,
) -> tuple[TelegramConfig, DiscordConfig, VKConfig]:
    telegram_config = TelegramConfig(
        api_token=settings.telegram.api_token.get_secret_value(),
        chat_id=settings.telegram.chat_id,
        message_text=notification.text,
        image=notification.image,
        has_spoiler=notification.image_spoiler,
    )

    discord_embed = _get_discord_embed(notification)

    discord_config = DiscordConfig(
        api_token=settings.discord.api_token.get_secret_value(),
        channel_id=settings.discord.chat_id,
        message_text=notification.text,
        image=notification.image if isinstance(notification.image, bytes) else None,
        roles_to_mention=notification.roles_to_mention,
        users_to_mention=notification.users_to_mention,
        embed=discord_embed,
    )

    vk_config = VKConfig()  # TODO: add vk support

    return telegram_config, discord_config, vk_config


def format_report(report: SendReport) -> str:  # TODO: add tests
    return REPORT_TEMPLATE.format(
        report="\n".join([
            "{} {}{}".format(
                EMOJI_TO_STATUS[platform.status],
                platform.name.value.capitalize(),
                f": {platform.error_message}" if platform.status == Status.FAILED else "",
            )
            for platform in [report.telegram, report.discord, report.vk]
        ]),
    )
