from enum import Enum


class ConfirmationofpayeeJsonOutboundCopRequestAccountType(str, Enum):
    BUSINESS = "BUSINESS"
    PERSONAL = "PERSONAL"

    def __str__(self) -> str:
        return str(self.value)
