from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, SecretStr, ValidatorFunctionWrapHandler, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .types import Platform, Status
from .validators import validate_image

model_config = ConfigDict(
    extra="forbid",
    validate_assignment=True,
)

settings_config = SettingsConfigDict(
    env_file=".env",
    env_nested_delimiter="__",
    validate_default=True,
    extra="forbid",
    use_attribute_docstrings=True,
)


class PlatformSettings(BaseSettings):
    api_token: SecretStr
    chat_id: int


class NotifierSettings(BaseSettings):
    """Settings for notifier client."""
    discord: PlatformSettings
    telegram: PlatformSettings
    vk: PlatformSettings

    model_config = settings_config


class DiscordEmbed(BaseModel):
    title: str = ""
    description: str = ""
    image: HttpUrl | bytes | None = None

    @field_validator("image", mode="wrap")
    @classmethod
    def get_image(cls, value: str | None, handler: ValidatorFunctionWrapHandler) -> str | bytes | HttpUrl | None:
        return validate_image(value, handler)


class Notification(BaseModel):
    text: str = ""
    """Message text."""
    image: str | HttpUrl | bytes | None = None
    """Main image."""
    image_spoiler: bool = False

    embeds: list[DiscordEmbed] = Field(default_factory=list)

    roles_to_mention: list[str] = Field(default_factory=list)
    users_to_mention: list[str] = Field(default_factory=list)

    model_config = model_config

    @field_validator("image", mode="wrap")
    @classmethod
    def get_image(cls, value: str | None, handler: ValidatorFunctionWrapHandler) -> str | bytes | HttpUrl | None:
        return validate_image(value, handler)


class PlatformReport(BaseModel):
    name: Platform
    status: Status = Status.IN_PROGRESS
    error_message: str = ""
    response: dict[str, Any] | None = None

    model_config = model_config


class SendReport(BaseModel):
    telegram: PlatformReport
    discord: PlatformReport
    vk: PlatformReport

    model_config = model_config
