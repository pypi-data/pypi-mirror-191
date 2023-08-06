from enum import Enum


class PispgatewayDestinationType(str, Enum):
    SCAN = "SCAN"
    ACCOUNT = "ACCOUNT"

    def __str__(self) -> str:
        return str(self.value)
