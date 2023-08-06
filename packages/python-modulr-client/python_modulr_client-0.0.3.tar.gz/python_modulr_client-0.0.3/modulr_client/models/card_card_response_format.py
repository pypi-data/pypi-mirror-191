from enum import Enum


class CardCardResponseFormat(str, Enum):
    PHYSICAL = "PHYSICAL"
    VIRTUAL = "VIRTUAL"

    def __str__(self) -> str:
        return str(self.value)
