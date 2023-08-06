from enum import Enum


class AccountIdentifierCountrySpecificDetailsResponseBankCodeType(str, Enum):
    ABA = "ABA"
    CHIPS = "CHIPS"

    def __str__(self) -> str:
        return str(self.value)
