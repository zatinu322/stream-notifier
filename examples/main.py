import asyncio

from stream_notifier.extras import (
    NotifierSettings,
    Platform,
    format_report,
    get_platform_configs,
    load_notification_from_yaml,
    send_notifications,
)


async def main() -> None:
    # load api tokens and chat IDs
    settings = NotifierSettings()
    # load notification config
    notification = load_notification_from_yaml("notification.yaml")
    # generate platform configs
    telegram_config, discord_config, vk_config = get_platform_configs(settings, notification)

    # send notifications
    report = await send_notifications(
        discord_config=discord_config,
        telegram_config=telegram_config,
        # vk_config=vk_config,  # TODO: add vk support
        ignored_platforms=[Platform.TELEGRAM, Platform.DISCORD, Platform.VK],
    )

    # show pretty report
    print(format_report(report))


if __name__ == "__main__":
    asyncio.run(main())
