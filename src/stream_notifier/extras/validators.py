from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import HttpUrl, ValidatorFunctionWrapHandler

if TYPE_CHECKING:
    from .schemas import Notification


def validate_image(value: str | None, handler: ValidatorFunctionWrapHandler) -> str | bytes | HttpUrl | None:
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


def validate_discord_message_text_ommiting(model: "Notification") -> "Notification":
    if model.send_discord_text:
        return model

    if model.image or model.embeds:
        return model

    raise ValueError("You should provide image or embed info when sending message text is omitted.")
