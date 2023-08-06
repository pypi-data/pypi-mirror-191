from enum import Enum


class DirectdebitoutboundEnquiryMandateResponseAuddisIndicator(str, Enum):
    N = "N"
    A = "A"

    def __str__(self) -> str:
        return str(self.value)
