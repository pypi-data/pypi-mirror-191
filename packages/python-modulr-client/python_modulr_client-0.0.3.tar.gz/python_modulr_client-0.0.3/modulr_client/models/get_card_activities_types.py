from enum import Enum


class GetCardActivitiesTypes(str, Enum):
    REVERSAL = "REVERSAL"
    SETTLEMENT = "SETTLEMENT"
    AUTHORISATION = "AUTHORISATION"
    REFUND = "REFUND"

    def __str__(self) -> str:
        return str(self.value)
