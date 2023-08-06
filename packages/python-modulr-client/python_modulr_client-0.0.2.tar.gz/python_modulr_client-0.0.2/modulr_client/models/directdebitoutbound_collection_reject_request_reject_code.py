from enum import Enum


class DirectdebitoutboundCollectionRejectRequestRejectCode(str, Enum):
    SKIP_DEBIT_ATTEMPT = "SKIP_DEBIT_ATTEMPT"
    AMOUNT_NOT_YET_DUE = "AMOUNT_NOT_YET_DUE"
    ADVANCE_NOTICE_DISPUTED = "ADVANCE_NOTICE_DISPUTED"
    PRESENTATION_OVERDUE = "PRESENTATION_OVERDUE"
    AMOUNT_DIFFERS = "AMOUNT_DIFFERS"

    def __str__(self) -> str:
        return str(self.value)
