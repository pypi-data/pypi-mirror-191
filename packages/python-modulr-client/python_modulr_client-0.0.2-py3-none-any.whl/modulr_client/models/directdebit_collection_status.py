from enum import Enum


class DirectdebitCollectionStatus(str, Enum):
    REPRESENTED = "REPRESENTED"
    SCHEDULED = "SCHEDULED"
    FAILED = "FAILED"
    REPRESENTABLE = "REPRESENTABLE"
    CANCELLED = "CANCELLED"
    SUCCESS = "SUCCESS"
    PROCESSING = "PROCESSING"

    def __str__(self) -> str:
        return str(self.value)
