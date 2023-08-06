from enum import Enum


class PispgatewayStandingOrderPaymentAmountCurrency(str, Enum):
    GBP = "GBP"

    def __str__(self) -> str:
        return str(self.value)
