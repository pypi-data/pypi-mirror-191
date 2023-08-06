from enum import Enum


class NotificationNotificationRequestChannel(str, Enum):
    EMAIL = "EMAIL"
    WEBHOOK = "WEBHOOK"

    def __str__(self) -> str:
        return str(self.value)
