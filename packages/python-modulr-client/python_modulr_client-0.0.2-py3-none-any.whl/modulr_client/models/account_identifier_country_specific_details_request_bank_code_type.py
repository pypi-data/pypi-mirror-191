from enum import Enum


class AccountIdentifierCountrySpecificDetailsRequestBankCodeType(str, Enum):
    ABA = "ABA"
    CHIPS = "CHIPS"

    def __str__(self) -> str:
        return str(self.value)
