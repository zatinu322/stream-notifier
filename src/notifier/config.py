from pydantic import BaseModel, Field, HttpUrl, PositiveInt, SecretStr


class DiscordEmbedImage(BaseModel):
    url: HttpUrl
    """Attachment or direct url."""
    description: str = ""
    """Image description."""


class DiscordEmbed(BaseModel):
    title: str = ""
    """Embed title."""
    description: str = ""
    """Embed description."""
    image: DiscordEmbedImage | None = None
    """Embed image."""

    roles_to_metion: list[str] = Field(default_factory=list)
    """Roles to be mentioned in Discord message."""
    users_to_metion: list[str] = Field(default_factory=list)
    """Users to be mentioned in Discord message."""


class DiscordConfig(BaseModel):
    api_token: SecretStr
    """Discord API token."""
    channel_id: PositiveInt
    """Discord channel ID for sending notifications."""

    message_text: str = ""
    """Discord message text."""

    message_image: HttpUrl | bytes | None = None
    """Discord message image."""

    embed: DiscordEmbed | None = None
    """Discord embed."""


class TelegramConfig(BaseModel):
    api_token: SecretStr
    """Telegram Bot API token."""

    chat_id: int
    """Telegram chat ID for sending notifications."""
    message_text: str = ""
    """Telegram message text."""

    image: str | HttpUrl | bytes | None = None
    """Notification image."""
    has_spoiler: bool = False
    """Hide image with spoiler."""
