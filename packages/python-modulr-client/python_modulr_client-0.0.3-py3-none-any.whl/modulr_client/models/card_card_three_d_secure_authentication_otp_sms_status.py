from enum import Enum


class CardCardThreeDSecureAuthenticationOtpSmsStatus(str, Enum):
    ENROLLED = "ENROLLED"
    NOT_ENROLLED = "NOT_ENROLLED"
    UNENROLLED = "UNENROLLED"

    def __str__(self) -> str:
        return str(self.value)
