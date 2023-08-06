from enum import Enum


class PaymentRegulatoryReportingType(str, Enum):
    DEBT = "DEBT"
    BOTH = "BOTH"
    CRED = "CRED"

    def __str__(self) -> str:
        return str(self.value)
