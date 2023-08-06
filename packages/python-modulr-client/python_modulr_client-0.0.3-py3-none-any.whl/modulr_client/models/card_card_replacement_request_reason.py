from enum import Enum


class CardCardReplacementRequestReason(str, Enum):
    STOLEN = "STOLEN"
    RENEW = "RENEW"
    LOST = "LOST"
    DAMAGED = "DAMAGED"

    def __str__(self) -> str:
        return str(self.value)
