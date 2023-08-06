from enum import Enum


class CardCardResponseStatus(str, Enum):
    EXPIRED = "EXPIRED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CREATED = "CREATED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"

    def __str__(self) -> str:
        return str(self.value)
