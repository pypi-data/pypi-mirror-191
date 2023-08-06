from enum import Enum


class NotificationNotificationConfigTimesToRunItem(str, Enum):
    PM = "PM"
    AM = "AM"

    def __str__(self) -> str:
        return str(self.value)
