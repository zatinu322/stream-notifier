from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from stream_notifier.shared import request_model_config, response_model_config


class TelegramUser(BaseModel):
    id: int
    is_bot: bool
    first_name: str = ""
    username: str = ""

    model_config = response_model_config


class TelegramMessageEntity(BaseModel):
    type: str
    offset: int
    length: int

    url: str | None = None
    user: TelegramUser | None = None
    language: str | None = None

    custom_emoji_id: str | None = None
    unix_time: int | None = None
    date_time_format: str | None = None

    model_config = response_model_config


class TelegramSendMessageRequest(BaseModel):
    chat_id: int | str

    text: str = Field(min_length=1, max_length=4096)
    entities: str | None = None
    """JSON-строка."""

    model_config = request_model_config


class TelegramSendPhotoRequest(BaseModel):
    chat_id: int | str

    photo: str | None = None
    has_spoiler: bool = False

    caption: str = Field("", max_length=1024)
    caption_entities: str | None = None
    """JSON-строка."""

    model_config = request_model_config


class TelegramChat(BaseModel):
    id: int
    first_name: str = ""
    username: str = ""
    type: Literal["private", "group", "supergroup", "channel"]

    model_config = response_model_config


class TelegramBaseChatResponse(BaseModel):
    message_id: int
    from_: TelegramUser = Field(alias="from")
    chat: TelegramChat
    date: datetime


class TelegramSendMessageResponse(TelegramBaseChatResponse):
    text: str

    model_config = response_model_config


class TelegramPhoto(BaseModel):
    file_id: str
    file_unique_id: str

    file_size: int
    width: int
    height: int

    model_config = response_model_config


class TelegramSendPhotoResponse(TelegramBaseChatResponse):
    photo: list[TelegramPhoto]
    caption: str = ""

    model_config = response_model_config


class TelegramResponse(BaseModel):
    ok: bool
    result: TelegramSendMessageResponse | TelegramSendPhotoResponse

    model_config = response_model_config
