from enum import StrEnum


class Platform(StrEnum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    VK = "vk"


class Status(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    IGNORED = "ignored"
