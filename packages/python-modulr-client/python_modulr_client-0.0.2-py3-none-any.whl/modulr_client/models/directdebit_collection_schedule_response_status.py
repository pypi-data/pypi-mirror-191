from enum import Enum


class DirectdebitCollectionScheduleResponseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"

    def __str__(self) -> str:
        return str(self.value)
