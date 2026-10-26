from httpx import Response


class TelegramNotificationError(Exception):
    ...


class DiscordNotificationError(Exception):
    ...


class NotifierHTTPStatusError(Exception):
    def __init__(self, response: Response, message: str) -> None:
        self.message = message
        self.response = response

    def __str__(self) -> str:
        return f"Bad response code: {self.response.status_code}. Full response: {self.response.text}. {self.message}"
