from enum import Enum


class AccountAccountResponseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLIENT_BLOCKED = "CLIENT_BLOCKED"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"

    def __str__(self) -> str:
        return str(self.value)
