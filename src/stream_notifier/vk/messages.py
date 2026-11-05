from typing import TYPE_CHECKING

from telegram_markdown import parse_markdown_to_entities

from stream_notifier.exceptions import VKNotificationError
from stream_notifier.shared import raise_for_status

from .schemas import VKSendMessageRequest, VKSendMessageResponse

if TYPE_CHECKING:
    from stream_notifier.client import NotifierClient


async def send_vk_notification(client: "NotifierClient") -> VKSendMessageResponse:
    if not client.vk_config:
        raise VKNotificationError("No VK config provided.")

    raw_text, _ = parse_markdown_to_entities(client.vk_config.message_text)

    headers = {
        "Authorization": f"Bearer {client.vk_config.api_token.get_secret_value()}",
    }
    payload = VKSendMessageRequest(
        message=raw_text,
        from_group=1,
        owner_id=client.vk_config.group_id,
    ).model_dump()

    response = await client.request(
        method="POST",
        url="https://api.vk.com/method/wall.post",
        data=payload,
        headers=headers,
    )
    raise_for_status(response)
    return VKSendMessageResponse.model_validate(response.json())
