from enum import Enum


class CardAsyncTaskResponseType(str, Enum):
    PHYSICAL_CARD_CREATE = "PHYSICAL_CARD_CREATE"

    def __str__(self) -> str:
        return str(self.value)
