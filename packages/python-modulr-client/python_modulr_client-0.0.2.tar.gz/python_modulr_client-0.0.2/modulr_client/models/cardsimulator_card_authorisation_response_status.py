from enum import Enum


class CardsimulatorCardAuthorisationResponseStatus(str, Enum):
    APPROVED = "APPROVED"
    SETTLED = "SETTLED"
    REVERSED = "REVERSED"

    def __str__(self) -> str:
        return str(self.value)
