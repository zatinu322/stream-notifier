from httpx import AsyncClient, RequestError
from tenacity import RetryError, retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from stream_notifier.config import DiscordConfig, TelegramConfig, VKConfig
from stream_notifier.discord.messages import send_discord_notification
from stream_notifier.discord.schemas import DiscordSendMessageResponse
from stream_notifier.exceptions import DiscordNotificationError, TelegramNotificationError, VKNotificationError
from stream_notifier.telegram.messages import send_photo_to_telegram, send_text_to_telegram
from stream_notifier.telegram.schemas import TelegramResponse
from stream_notifier.vk.messages import send_vk_notification
from stream_notifier.vk.schemas import VKSendMessageResponse


class NotifierClient(AsyncClient):
    def __init__(  # type: ignore[no-untyped-def]
        self,
        telegram_config: TelegramConfig | None = None,
        discord_config: DiscordConfig | None = None,
        vk_config: VKConfig | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.telegram_config = telegram_config
        self.discord_config = discord_config
        self.vk_config = vk_config

    async def send_discord(self) -> DiscordSendMessageResponse:
        if not self.discord_config:
            raise DiscordNotificationError("No discord config provided.")

        try:
            return await send_discord_notification(self.discord_config, self)  # TODO: remove config
        except (RequestError, RetryError) as e:
            raise DiscordNotificationError from e

    async def send_telegram(self) -> TelegramResponse:
        if not self.telegram_config:
            raise TelegramNotificationError("No Telegram config provided.")

        try:
            if self.telegram_config.image:
                return await send_photo_to_telegram(self.telegram_config, self)  # TODO: remove config
            return await send_text_to_telegram(self.telegram_config, self)
        except (RequestError, RetryError) as e:
            raise TelegramNotificationError from e

    async def send_vk(self) -> VKSendMessageResponse:
        try:
            return await send_vk_notification(self)
        except (RequestError, RetryError) as e:
            raise VKNotificationError from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=(retry_if_exception_type(RequestError)),
        reraise=True,
    )
    async def request(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        return await super().request(*args, **kwargs)
