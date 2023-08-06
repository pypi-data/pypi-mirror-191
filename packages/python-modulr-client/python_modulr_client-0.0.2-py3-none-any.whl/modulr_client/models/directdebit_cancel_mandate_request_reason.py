from enum import Enum


class DirectdebitCancelMandateRequestReason(str, Enum):
    INSTRUCTION_CANCELLED_PAYER = "INSTRUCTION_CANCELLED_PAYER"
    SERVICE_ENDED = "SERVICE_ENDED"
    INSTRUCTION_CANCELLED_PAYEE = "INSTRUCTION_CANCELLED_PAYEE"

    def __str__(self) -> str:
        return str(self.value)
