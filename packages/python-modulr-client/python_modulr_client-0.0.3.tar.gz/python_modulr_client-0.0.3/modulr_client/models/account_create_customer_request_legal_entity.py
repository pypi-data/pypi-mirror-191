from enum import Enum


class AccountCreateCustomerRequestLegalEntity(str, Enum):
    NL = "NL"
    GB = "GB"
    IE = "IE"

    def __str__(self) -> str:
        return str(self.value)
