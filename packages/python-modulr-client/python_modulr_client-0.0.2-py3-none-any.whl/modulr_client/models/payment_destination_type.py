from enum import Enum


class PaymentDestinationType(str, Enum):
    ACCOUNT = "ACCOUNT"
    IBAN = "IBAN"
    SCAN = "SCAN"
    BENEFICIARY = "BENEFICIARY"

    def __str__(self) -> str:
        return str(self.value)
