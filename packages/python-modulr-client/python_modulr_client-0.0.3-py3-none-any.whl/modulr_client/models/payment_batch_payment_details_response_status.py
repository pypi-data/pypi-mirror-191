from enum import Enum


class PaymentBatchPaymentDetailsResponseStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

    def __str__(self) -> str:
        return str(self.value)
