from enum import Enum


class AccountCustomerLegalEntity(str, Enum):
    NL = "NL"
    GB = "GB"
    IE = "IE"

    def __str__(self) -> str:
        return str(self.value)
