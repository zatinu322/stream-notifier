from pathlib import Path

from pydantic import HttpUrl, ValidatorFunctionWrapHandler


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
