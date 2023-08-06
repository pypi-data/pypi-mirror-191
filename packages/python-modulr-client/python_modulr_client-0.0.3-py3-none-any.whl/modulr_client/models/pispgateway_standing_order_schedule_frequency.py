from enum import Enum


class PispgatewayStandingOrderScheduleFrequency(str, Enum):
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"

    def __str__(self) -> str:
        return str(self.value)
