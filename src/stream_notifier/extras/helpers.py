import yaml
from pydantic import HttpUrl

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig, TelegramConfig, VKConfig

from .schemas import Notification, NotifierSettings, SendReport
from .types import Status

REPORT_TEMPLATE = "Отчёт об отправке уведомлений.\n\n{report}\n"

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


def _get_discord_embeds(notification: Notification) -> list[DiscordEmbedConfig]:
    if not notification.embeds:
        return []

    embeds = [
        DiscordEmbedConfig(
            title=embed.title,
            description=embed.description,
            image=embed.image if isinstance(embed.image, (HttpUrl, bytes)) else None,
        ) for embed in notification.embeds
    ]

    return [embed for embed in embeds if any((embed.title, embed.description, embed.image))]


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

    discord_embeds = _get_discord_embeds(notification)

    discord_config = DiscordConfig(
        api_token=settings.discord.api_token.get_secret_value(),
        channel_id=settings.discord.chat_id,
        message_text=notification.text,
        image=notification.image if isinstance(notification.image, bytes) else None,
        roles_to_mention=notification.roles_to_mention,
        users_to_mention=notification.users_to_mention,
        embeds=discord_embeds,
    )

    vk_config = VKConfig(
        api_token=settings.vk.api_token.get_secret_value(),
        group_id=settings.vk.chat_id,
        message_text=notification.text,
    )

    return telegram_config, discord_config, vk_config


def format_report(report: SendReport) -> str:
    return REPORT_TEMPLATE.format(
        report="\n".join([
            "{} {}{}".format(
                EMOJI_TO_STATUS[platform.status],
                platform.name.value.capitalize(),
                f": {platform.error_message}" if platform.error_message else "",
            )
            for platform in [report.telegram, report.discord, report.vk]
        ]),
    )
