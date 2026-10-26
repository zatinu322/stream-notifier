from httpx import AsyncClient, RequestError
from tenacity import RetryError, retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from notifier.config import DiscordConfig, TelegramConfig
from notifier.discord.schemas import DiscordSendMessageRequest
from notifier.exceptions import DiscordNotificationError, TelegramNotificationError
from notifier.telegram.messages import send_photo_to_telegram, send_text_to_telegram
from notifier.telegram.schemas import TelegramResponse


class NotifierClient(AsyncClient):
    def __init__(  # type: ignore[no-untyped-def]
        self,
        telegram_config: TelegramConfig | None = None,
        discord_config: DiscordConfig | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.telegram_config = telegram_config
        self.discord_config = discord_config

    async def send_discord(self) -> None:
        if not self.discord_config:
            raise DiscordNotificationError("No discord config provided.")

        try:
            url = f"https://discord.com/api/v10/channels/{self.discord_config.channel_id}/messages"
            headers = {
                "Authorization": f"Bot {self.discord_config.api_token.get_secret_value()}",
            }
            payload = DiscordSendMessageRequest(
                content=self.discord_config.message_text,
            ).model_dump()
            response = await self.request(
                method="POST",
                url=url,
                data=payload,
                headers=headers,
            )
            print(response.text)
        except (RequestError, RetryError) as e:
            raise DiscordNotificationError from e

    async def send_telegram(self) -> TelegramResponse:
        if not self.telegram_config:
            raise TelegramNotificationError("No Telegram config provided.")

        try:
            if self.telegram_config.image:
                return await send_photo_to_telegram(self.telegram_config, self)
            return await send_text_to_telegram(self.telegram_config, self)
        except (RequestError, RetryError) as e:
            raise TelegramNotificationError from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=(retry_if_exception_type(RequestError)),
        reraise=True,
    )
    async def request(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        return await super().request(*args, **kwargs)
