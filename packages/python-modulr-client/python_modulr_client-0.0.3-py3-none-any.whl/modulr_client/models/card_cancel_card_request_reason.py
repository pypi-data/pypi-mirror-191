from enum import Enum


class CardCancelCardRequestReason(str, Enum):
    STOLEN = "STOLEN"
    DESTROYED = "DESTROYED"
    LOST = "LOST"

    def __str__(self) -> str:
        return str(self.value)
