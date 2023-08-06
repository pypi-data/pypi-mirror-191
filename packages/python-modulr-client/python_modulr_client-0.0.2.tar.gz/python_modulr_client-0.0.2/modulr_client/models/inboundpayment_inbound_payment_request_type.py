from enum import Enum


class InboundpaymentInboundPaymentRequestType(str, Enum):
    PI_SEPA_INST = "PI_SEPA_INST"
    PI_SECT = "PI_SECT"
    INT_INTERC = "INT_INTERC"
    PI_FP = "PI_FP"
    PO_REV = "PO_REV"
    PI_BACS = "PI_BACS"
    PI_DD = "PI_DD"
    PI_FAST = "PI_FAST"
    PI_CHAPS = "PI_CHAPS"

    def __str__(self) -> str:
        return str(self.value)
