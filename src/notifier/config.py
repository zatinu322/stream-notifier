from pydantic import BaseModel, HttpUrl, SecretStr


class DiscordConfig(BaseModel):
    ...


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
