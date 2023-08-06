from enum import Enum


class AccountCreateCustomerRequestType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    PLC = "PLC"
    PCM_INDIVIDUAL = "PCM_INDIVIDUAL"
    LPARTNRSHP = "LPARTNRSHP"
    SOLETRADER = "SOLETRADER"
    LLP = "LLP"
    PCM_BUSINESS = "PCM_BUSINESS"
    OPARTNRSHP = "OPARTNRSHP"
    CHARITY = "CHARITY"
    LLC = "LLC"
    TRUST = "TRUST"

    def __str__(self) -> str:
        return str(self.value)
