from enum import Enum


class GetCustomerStatusesItem(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return str(self.value)
