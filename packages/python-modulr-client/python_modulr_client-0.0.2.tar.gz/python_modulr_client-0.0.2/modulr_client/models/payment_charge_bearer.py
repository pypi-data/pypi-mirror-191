from enum import Enum


class PaymentChargeBearer(str, Enum):
    SHAR = "SHAR"
    DEBT = "DEBT"
    CRED = "CRED"

    def __str__(self) -> str:
        return str(self.value)
