from enum import Enum


class AccountAdditionalPersonalIdentifierResponseType(str, Enum):
    BSN = "BSN"

    def __str__(self) -> str:
        return str(self.value)
