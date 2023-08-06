from enum import Enum


class AccountPendingTransactionResponseType(str, Enum):
    INT_INTERC = "INT_INTERC"
    PO_DD = "PO_DD"
    PI_MASTER = "PI_MASTER"
    PI_FAST_REV = "PI_FAST_REV"
    PI_VISA = "PI_VISA"
    PO_SWIFT = "PO_SWIFT"
    FE_ACMNT = "FE_ACMNT"
    PO_VISA = "PO_VISA"
    PO_SECT = "PO_SECT"
    PI_SEPA_INST = "PI_SEPA_INST"
    FE_ACOPN = "FE_ACOPN"
    ADHOC = "ADHOC"
    PO_REV = "PO_REV"
    FE_REV = "FE_REV"
    PO_MASTER = "PO_MASTER"
    PI_DD = "PI_DD"
    PI_REV = "PI_REV"
    PI_FAST = "PI_FAST"
    PI_SECT = "PI_SECT"
    PO_SEPA_INST = "PO_SEPA_INST"
    PO_CHAPS = "PO_CHAPS"
    INT_INTRAC = "INT_INTRAC"
    PO_FAST = "PO_FAST"
    PI_CHAPS = "PI_CHAPS"
    FE_TXN = "FE_TXN"
    PI_BACS_CONTRA = "PI_BACS_CONTRA"
    PO_REV_MASTER = "PO_REV_MASTER"
    PI_SWIFT = "PI_SWIFT"
    PI_BACS = "PI_BACS"

    def __str__(self) -> str:
        return str(self.value)
