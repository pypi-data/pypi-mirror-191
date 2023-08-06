from enum import Enum


class AccountAdditionalAssociateIdentifierType(str, Enum):
    BSN = "BSN"

    def __str__(self) -> str:
        return str(self.value)
