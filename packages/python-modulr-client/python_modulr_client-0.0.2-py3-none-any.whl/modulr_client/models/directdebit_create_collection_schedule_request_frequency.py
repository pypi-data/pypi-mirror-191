from enum import Enum


class DirectdebitCreateCollectionScheduleRequestFrequency(str, Enum):
    ONCE = "ONCE"
    EVERY_TWO_WEEKS = "EVERY_TWO_WEEKS"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    ANNUALLY = "ANNUALLY"
    EVERY_FOUR_WEEKS = "EVERY_FOUR_WEEKS"
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"
    QUARTERLY = "QUARTERLY"

    def __str__(self) -> str:
        return str(self.value)
