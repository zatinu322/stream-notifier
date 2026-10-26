from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from notifier.shared import request_model_config


class DiscordEmbedImage(BaseModel):
    url: HttpUrl | str
    description: str = ""
    width: int | None = None
    height: int | None = None


class DiscordEmbed(BaseModel):
    title: str = ""
    description: str = ""
    type: Literal["rich", "image"] = "rich"
    image: DiscordEmbedImage | None = None

    model_config = request_model_config


class DiscordSendMessageRequest(BaseModel):
    content: str = ""
    embeds: list[DiscordEmbed] = Field(default_factory=list)

    model_config = request_model_config
