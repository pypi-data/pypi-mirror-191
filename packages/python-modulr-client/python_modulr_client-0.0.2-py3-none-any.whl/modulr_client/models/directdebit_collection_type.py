from enum import Enum


class DirectdebitCollectionType(str, Enum):
    INDEMNITY = "INDEMNITY"
    COLLECTION = "COLLECTION"

    def __str__(self) -> str:
        return str(self.value)
