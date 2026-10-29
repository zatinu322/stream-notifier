import asyncio
from pathlib import Path

from stream_notifier import (
    DiscordConfig,
    DiscordEmbedConfig,
    NotifierClient,
    TelegramConfig,
    # VKConfig,
)

REQUEST_TIMEOUT = 60


async def main() -> None:
    image_bytes = Path("examples/example.png").read_bytes()
    message_text = "||Hello, world!||"

    telegram_config = TelegramConfig(
        api_token="token",
        chat_id=123,
        message_text=message_text,
        image=image_bytes,
        has_spoiler=True,
    )

    discord_config = DiscordConfig(
        api_token="token",
        channel_id=123,
        message_text=message_text,
        image=image_bytes,
        embed=DiscordEmbedConfig(
            title="Hello!",
            description="World!",
            image="https://example.com",
        ),
        roles_to_mention=["123", "456"],
        users_to_mention=["789", "123"],
    )

    # vk_config = VKConfig()  TODO: Add vk support

    async with NotifierClient(
        telegram_config=telegram_config,
        discord_config=discord_config,
        timeout=REQUEST_TIMEOUT,
        # vk_config=vk_config,  TODO: Add vk support
    ) as client:
        client.send_telegram()
        client.send_discord()
        # TODO: Add vk support


if __name__ == "__main__":
    asyncio.run(main())
