import json
from typing import TYPE_CHECKING

from pydantic import HttpUrl

from stream_notifier.config import DiscordConfig, DiscordEmbedConfig
from stream_notifier.discord.schemas import (
    DiscordEmbed,
    DiscordEmbedImage,
    DiscordSendMessageRequest,
    DiscordSendMessageResponse,
)
from stream_notifier.exceptions import DiscordNotificationError
from stream_notifier.shared import MultipartFormData, raise_for_status

if TYPE_CHECKING:
    from stream_notifier.client import NotifierClient


def _get_discord_embeds(
    embed_configs: list[DiscordEmbedConfig],
) -> tuple[list[DiscordEmbed], MultipartFormData]:  # TODO: adjust tests, add multiple embeds
    if not embed_configs:
        return [], {}

    multipart_data: MultipartFormData = {}
    embeds = []
    for embed_index, embed_config in enumerate(embed_configs):
        embed_type = "rich"
        embed_image_url = ""
        if embed_image := embed_config.image:
            embed_type = "image"
            if isinstance(embed_image, bytes):
                embed_image_url = f"attachment://embed{embed_index}.png"
                multipart_data[f"files[{embed_index}]"] = (f"embed{embed_index}.png", embed_image, "image/png")
            elif isinstance(embed_image, HttpUrl):
                embed_image_url = str(embed_image)

        embeds.append(DiscordEmbed(
            title=embed_config.title,
            description=embed_config.description,
            type=embed_type,
            image=DiscordEmbedImage(url=embed_image_url) if embed_image_url else None,
        ))

    return embeds, multipart_data


def _get_message_text(discord_config: DiscordConfig) -> str:
    user_mentions = [f"<@{user_id}>" for user_id in discord_config.users_to_mention]
    role_mentions = [f"<@&{role_id}>" for role_id in discord_config.roles_to_mention]
    mentions = " ".join(user_mentions + role_mentions)
    return f"{mentions}\n{discord_config.message_text}" if mentions else discord_config.message_text


def _get_image(image: bytes | None, embeds: list[DiscordEmbed]) -> MultipartFormData | None:  # TODO: Add tests
    if not image:
        return None

    image_index = len([embed for embed in embeds if embed.image])
    return {
        f"files[{image_index}]": ("image.png", image, "image/png"),
    }


async def send_discord_notification(client: "NotifierClient") -> DiscordSendMessageResponse:
    if not client.discord_config:
        raise DiscordNotificationError("No discord config provided.")

    embeds, multipart_data = _get_discord_embeds(client.discord_config.embeds)

    if image_multipart := _get_image(client.discord_config.image, embeds):
        multipart_data |= image_multipart

    url = f"https://discord.com/api/v10/channels/{client.discord_config.channel_id}/messages"
    headers = {
        "Authorization": f"Bot {client.discord_config.api_token.get_secret_value()}",
    }

    payload = DiscordSendMessageRequest(
        content=_get_message_text(client.discord_config),
        embeds=embeds if embeds else [],
    ).model_dump()

    response = await client.request(
        method="POST",
        url=url,
        data={"payload_json": json.dumps(payload)},
        headers=headers,
        files=multipart_data if multipart_data else None,
    )
    raise_for_status(response)

    return DiscordSendMessageResponse.model_validate(response.json())
