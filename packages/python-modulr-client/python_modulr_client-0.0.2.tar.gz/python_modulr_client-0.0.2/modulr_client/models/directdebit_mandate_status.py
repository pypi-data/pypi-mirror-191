from enum import Enum


class DirectdebitMandateStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUBMITTED = "SUBMITTED"
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"

    def __str__(self) -> str:
        return str(self.value)
