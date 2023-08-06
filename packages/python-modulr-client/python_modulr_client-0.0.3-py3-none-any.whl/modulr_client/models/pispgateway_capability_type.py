from enum import Enum


class PispgatewayCapabilityType(str, Enum):
    SINGLE_IMMEDIATE = "SINGLE_IMMEDIATE"
    STANDING_ORDER = "STANDING_ORDER"

    def __str__(self) -> str:
        return str(self.value)
