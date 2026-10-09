from typing import TYPE_CHECKING

from notifier.config import TelegramConfig
from notifier.shared import raise_for_status
from notifier.telegram.schemas import (
    TelegramResponse,
    TelegramSendMessageRequest,
    TelegramSendPhotoRequest,
)

if TYPE_CHECKING:
    from notifier.client import NotifierClient


async def send_photo_to_telegram(
    telegram_config: TelegramConfig,
    client: "NotifierClient",
) -> TelegramResponse:
    image = telegram_config.image
    add_multipart = isinstance(image, bytes)

    api_token = telegram_config.api_token.get_secret_value()
    url = f"https://api.telegram.org/bot{api_token}/sendPhoto"
    payload = TelegramSendPhotoRequest(
        chat_id=telegram_config.chat_id,
        has_spoiler=telegram_config.has_spoiler,
        caption=telegram_config.message_text,
        photo=None if add_multipart else image,
        parse_mode=None,  # TODO: Add formatting
    ).model_dump(exclude_none=True)

    files = None
    if add_multipart:
        files = {
            "photo": ("image.png", image, "image/png"),
        }

    response = await client.send_request(
        method="POST",
        url=url,
        payload=payload,
        files=files,
    )
    raise_for_status(response)
    return TelegramResponse.model_validate(response.json())


async def send_text_to_telegram(
    telegram_config: TelegramConfig,
    client: "NotifierClient",
) -> TelegramResponse:
    api_token = telegram_config.api_token.get_secret_value()
    url = f"https://api.telegram.org/bot{api_token}/sendMessage"
    payload = TelegramSendMessageRequest(
        chat_id=telegram_config.chat_id,
        text=telegram_config.message_text,
        parse_mode=None,  # TODO: Add formatting
    ).model_dump(exclude_none=True)

    response = await client.send_request(method="POST", url=url, payload=payload)
    raise_for_status(response)
    return TelegramResponse.model_validate(response.json())
