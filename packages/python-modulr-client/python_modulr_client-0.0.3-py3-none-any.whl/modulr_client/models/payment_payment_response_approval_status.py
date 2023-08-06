from enum import Enum


class PaymentPaymentResponseApprovalStatus(str, Enum):
    NOTNEEDED = "NOTNEEDED"
    APPROVED = "APPROVED"
    DELETED = "DELETED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"

    def __str__(self) -> str:
        return str(self.value)
