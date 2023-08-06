from enum import Enum


class CardOneTimeTokenRequestPurpose(str, Enum):
    UPDATE = "UPDATE"
    READ = "READ"

    def __str__(self) -> str:
        return str(self.value)
