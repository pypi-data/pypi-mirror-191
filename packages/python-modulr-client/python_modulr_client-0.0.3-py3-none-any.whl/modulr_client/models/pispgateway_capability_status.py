from enum import Enum


class PispgatewayCapabilityStatus(str, Enum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    INACTIVE = "INACTIVE"

    def __str__(self) -> str:
        return str(self.value)
