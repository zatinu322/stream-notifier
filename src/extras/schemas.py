from typing import Any

from pydantic import BaseModel, ConfigDict

from .types import Platform, Status

model_config = ConfigDict(
    extra="forbid",
    validate_assignment=True,
)


class PlatformReport(BaseModel):
    platform: Platform
    status: Status = Status.IN_PROGRESS
    error_message: str = ""
    response: dict[str, Any] | None = None

    model_config = model_config


class SendReport(BaseModel):
    telegram: PlatformReport
    discord: PlatformReport
    vk: PlatformReport

    model_config = model_config
