from typing import Literal

from pydantic import BaseModel, Field

from stream_notifier.shared import request_model_config, response_model_config


class DiscordEmbedImage(BaseModel):
    url: str
    description: str = ""
    width: int | None = None
    height: int | None = None


class DiscordEmbed(BaseModel):
    title: str
    description: str
    type: Literal["rich", "image"] = "rich"
    image: DiscordEmbedImage | None = None

    model_config = request_model_config


class DiscordSendMessageRequest(BaseModel):
    content: str = ""
    embeds: list[DiscordEmbed] = Field(default_factory=list)

    model_config = request_model_config


class DiscordSendMessageResponse(BaseModel):
    id: str
    """Message ID."""
    type: int
    """Message type."""
    channel_id: str
    """Discord channel ID."""
    content: str = ""
    """Message text."""

    model_config = response_model_config
