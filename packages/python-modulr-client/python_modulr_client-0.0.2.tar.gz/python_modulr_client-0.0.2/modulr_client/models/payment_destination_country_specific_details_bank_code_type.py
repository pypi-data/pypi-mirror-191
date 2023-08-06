from enum import Enum


class PaymentDestinationCountrySpecificDetailsBankCodeType(str, Enum):
    ABA = "ABA"
    CHIPS = "CHIPS"

    def __str__(self) -> str:
        return str(self.value)
