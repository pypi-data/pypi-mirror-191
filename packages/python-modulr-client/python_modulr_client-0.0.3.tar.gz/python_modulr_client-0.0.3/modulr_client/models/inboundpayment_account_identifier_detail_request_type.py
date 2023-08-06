from enum import Enum


class InboundpaymentAccountIdentifierDetailRequestType(str, Enum):
    DD = "DD"
    SCAN = "SCAN"
    INTL = "INTL"
    IBAN = "IBAN"

    def __str__(self) -> str:
        return str(self.value)
