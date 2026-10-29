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
from stream_notifier.shared import raise_for_status

if TYPE_CHECKING:
    from stream_notifier.client import NotifierClient

MultipartFormData = dict[str, tuple[str, bytes, str]]


def _get_discord_embeds(
    embed_config: DiscordEmbedConfig | None,
    multipart_data: MultipartFormData,
) -> list[DiscordEmbed]:
    if not embed_config:
        return []

    embed_type = "rich"
    embed_image_url = ""
    if embed_image := embed_config.image:
        embed_type = "image"
        if isinstance(embed_image, bytes):
            embed_image_url = "attachment://embed.png"
            multipart_data["files[0]"] = ("embed.png", embed_image, "image/png")
        elif isinstance(embed_image, HttpUrl):
            embed_image_url = str(embed_image)

    return [
        DiscordEmbed(
            title=embed_config.title,
            description=embed_config.description,
            type=embed_type,
            image=DiscordEmbedImage(url=embed_image_url) if embed_image_url else None,
        ),
    ]


def _get_message_text(discord_config: DiscordConfig) -> str:
    user_mentions = [f"<@{user_id}>" for user_id in discord_config.users_to_mention]
    role_mentions = [f"<@&{role_id}>" for role_id in discord_config.roles_to_mention]
    mentions = " ".join(user_mentions + role_mentions)
    return f"{mentions}\n{discord_config.message_text}" if mentions else discord_config.message_text


async def send_discord_notification(
    discord_config: DiscordConfig,
    client: "NotifierClient",
) -> DiscordSendMessageResponse:
    multipart_data: MultipartFormData = {}
    embeds = _get_discord_embeds(discord_config.embed, multipart_data)

    if image := discord_config.image:
        multipart_data[f"files[{1 if embeds and embeds[0].image else 0}]"] = ("image.png", image, "image/png")

    url = f"https://discord.com/api/v10/channels/{discord_config.channel_id}/messages"
    headers = {
        "Authorization": f"Bot {discord_config.api_token.get_secret_value()}",
    }

    payload = DiscordSendMessageRequest(
        content=_get_message_text(discord_config),
        embeds=embeds if embeds else None,
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
