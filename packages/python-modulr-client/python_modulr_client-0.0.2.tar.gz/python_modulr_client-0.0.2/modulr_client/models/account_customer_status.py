from enum import Enum


class AccountCustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return str(self.value)
