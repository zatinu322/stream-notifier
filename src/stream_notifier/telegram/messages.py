import json
from typing import TYPE_CHECKING

from telegram_markdown import parse_markdown_to_entities

from stream_notifier.exceptions import TelegramNotificationError
from stream_notifier.shared import raise_for_status
from stream_notifier.telegram.schemas import (
    TelegramMessageEntity,
    TelegramResponse,
    TelegramSendMessageRequest,
    TelegramSendPhotoRequest,
)

if TYPE_CHECKING:
    from stream_notifier.client import NotifierClient


async def send_photo_to_telegram(client: "NotifierClient") -> TelegramResponse:
    if not client.telegram_config:
        raise TelegramNotificationError("No Telegram config provided.")

    image = client.telegram_config.image
    add_multipart = isinstance(image, bytes)

    plain_text, telegram_entities = parse_markdown_to_entities(client.telegram_config.message_text)

    api_token = client.telegram_config.api_token.get_secret_value()
    url = f"https://api.telegram.org/bot{api_token}/sendPhoto"
    payload = TelegramSendPhotoRequest(
        chat_id=client.telegram_config.chat_id,
        has_spoiler=client.telegram_config.has_spoiler,
        caption=plain_text,
        photo=None if add_multipart else image,
        caption_entities=json.dumps([
            TelegramMessageEntity.model_validate(entity).model_dump(exclude_none=True)
            for entity in telegram_entities
        ]),
    ).model_dump(exclude_none=True)

    files = None
    if add_multipart:
        files = {
            "photo": ("image.png", image, "image/png"),
        }

    response = await client.request(
        method="POST",
        url=url,
        data=payload,
        files=files,
    )
    raise_for_status(response)
    return TelegramResponse.model_validate(response.json())


async def send_text_to_telegram(client: "NotifierClient") -> TelegramResponse:
    if not client.telegram_config:
        raise TelegramNotificationError("No Telegram config provided.")

    plain_text, telegram_entities = parse_markdown_to_entities(client.telegram_config.message_text)

    api_token = client.telegram_config.api_token.get_secret_value()
    url = f"https://api.telegram.org/bot{api_token}/sendMessage"
    payload = TelegramSendMessageRequest(
        chat_id=client.telegram_config.chat_id,
        text=plain_text,
        entities=json.dumps([
            TelegramMessageEntity.model_validate(entity).model_dump(exclude_none=True)
            for entity in telegram_entities
        ]),
    ).model_dump(exclude_none=True)

    response = await client.request(method="POST", url=url, data=payload)
    raise_for_status(response)
    return TelegramResponse.model_validate(response.json())
