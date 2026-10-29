from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, SecretStr, ValidatorFunctionWrapHandler, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .types import Platform, Status

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


class Notification(BaseModel):
    text: str = ""
    """Message text."""
    image: str | HttpUrl | bytes | None = None
    """Main image."""
    image_spoiler: bool = False

    embed_title: str = ""
    embed_description: str = ""
    embed_image: HttpUrl | bytes | None = None

    roles_to_mention: list[str] = Field(default_factory=list)
    users_to_mention: list[str] = Field(default_factory=list)

    model_config = model_config

    @field_validator("image", "embed_image", mode="wrap")
    @classmethod
    def get_image(cls, value: str | None, handler: ValidatorFunctionWrapHandler) -> str | bytes | HttpUrl | None:
        if value is None:
            return None

        if not isinstance(value, str):
            return handler(value)

        if value.startswith(("http://", "https://")):
            return HttpUrl(value)

        image_path = Path(value)
        if image_path.exists():
            return image_path.read_bytes()

        return value


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
