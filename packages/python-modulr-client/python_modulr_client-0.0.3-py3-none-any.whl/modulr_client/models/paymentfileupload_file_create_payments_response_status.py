from enum import Enum


class PaymentfileuploadFileCreatePaymentsResponseStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    INVALID = "INVALID"
    DUPLICATE = "DUPLICATE"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    VALID = "VALID"
    PROCESSED = "PROCESSED"

    def __str__(self) -> str:
        return str(self.value)
