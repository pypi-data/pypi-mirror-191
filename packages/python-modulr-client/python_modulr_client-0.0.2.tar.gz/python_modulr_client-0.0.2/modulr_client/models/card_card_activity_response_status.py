from enum import Enum


class CardCardActivityResponseStatus(str, Enum):
    EXPIRED = "EXPIRED"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    SETTLED = "SETTLED"

    def __str__(self) -> str:
        return str(self.value)
