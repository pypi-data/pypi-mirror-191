from enum import Enum


class NotificationNotificationConfigDaysToRunItem(str, Enum):
    FRIDAY = "FRIDAY"
    TUESDAY = "TUESDAY"
    THURSDAY = "THURSDAY"
    SATURDAY = "SATURDAY"
    WEDNESDAY = "WEDNESDAY"
    MONDAY = "MONDAY"
    SUNDAY = "SUNDAY"

    def __str__(self) -> str:
        return str(self.value)
