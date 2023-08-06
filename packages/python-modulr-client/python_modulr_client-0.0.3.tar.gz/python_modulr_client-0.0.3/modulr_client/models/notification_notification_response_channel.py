from enum import Enum


class NotificationNotificationResponseChannel(str, Enum):
    EMAIL = "EMAIL"
    WEBHOOK = "WEBHOOK"

    def __str__(self) -> str:
        return str(self.value)
