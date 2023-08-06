from enum import Enum


class GetCustomersAssociateSearchCriteriaAssociateTypesItem(str, Enum):
    TRUST_BENEFICIARY = "TRUST_BENEFICIARY"
    PARTNER = "PARTNER"
    C_INTEREST = "C_INTEREST"
    INDIVIDUAL = "INDIVIDUAL"
    PCM_INDIVIDUAL = "PCM_INDIVIDUAL"
    SIGNATORY = "SIGNATORY"
    TRUST_SETTLOR = "TRUST_SETTLOR"
    SOLETRADER = "SOLETRADER"
    DIRECTOR = "DIRECTOR"
    TRUST_TRUSTEE = "TRUST_TRUSTEE"
    BENE_OWNER = "BENE_OWNER"
    CSECRETARY = "CSECRETARY"

    def __str__(self) -> str:
        return str(self.value)
