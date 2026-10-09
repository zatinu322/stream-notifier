from typing import Any

from httpx import AsyncClient, RequestError, Response  # type: ignore[import-not-found]
from tenacity import RetryError, retry, retry_if_exception_type, stop_after_attempt, wait_fixed  # type: ignore

from notifier.config import TelegramConfig
from notifier.exceptions import TelegramNotificationError
from notifier.telegram.messages import send_photo_to_telegram, send_text_to_telegram
from notifier.telegram.schemas import TelegramResponse


class NotifierClient(AsyncClient):
    def __init__(  # type: ignore[no-untyped-def]
        self,
        telegram_config: TelegramConfig | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.telegram_config = telegram_config

    async def send_telegram(self) -> TelegramResponse:
        if not self.telegram_config:
            raise TelegramNotificationError("No Telegram config provided.")

        try:
            if self.telegram_config.image:
                return await send_photo_to_telegram(self.telegram_config, self)
            return await send_text_to_telegram(self.telegram_config, self)
        except RetryError as e:
            raise TelegramNotificationError from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=(retry_if_exception_type(RequestError)),
    )
    async def send_request(
        self,
        method: str,
        url: str,
        payload: dict[str, Any],
        files: dict[str, Any] | None = None,
    ) -> Response:
        print(f"Request: {method}, {url}, {payload}")
        return await self.request(method, url, data=payload, files=files)
