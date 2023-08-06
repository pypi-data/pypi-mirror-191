from enum import Enum


class PispgatewayLegacyPaymentContextPaymentContextCode(str, Enum):
    Party_To_Party = "PartyToParty"
    Other = "Other"
    Ecommerce_Services = "EcommerceServices"
    PARTYTOPARTY = "PARTYTOPARTY"
    BILLPAYMENT = "BILLPAYMENT"
    ECOMMERCEGOODS = "ECOMMERCEGOODS"
    ECOMMERCESERVICES = "ECOMMERCESERVICES"
    OTHER = "OTHER"
    Bill_Payment = "BillPayment"
    Ecommerce_Goods = "EcommerceGoods"

    def __str__(self) -> str:
        return str(self.value)
