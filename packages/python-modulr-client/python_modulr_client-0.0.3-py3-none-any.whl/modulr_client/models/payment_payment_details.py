from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PaymentPaymentDetails")


@attr.s(auto_attribs=True)
class PaymentPaymentDetails:
    """
    Attributes:
        amount (float): Amount of currency that the payment is in Example: 1000.45.
        currency (str): ISO 4217 currency code that the amount is in Example: GBP.
        exchange_rate (float): Exchange rate Example: 1.45.
    """

    amount: float
    currency: str
    exchange_rate: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        currency = self.currency
        exchange_rate = self.exchange_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "currency": currency,
                "exchangeRate": exchange_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount")

        currency = d.pop("currency")

        exchange_rate = d.pop("exchangeRate")

        payment_payment_details = cls(
            amount=amount,
            currency=currency,
            exchange_rate=exchange_rate,
        )

        payment_payment_details.additional_properties = d
        return payment_payment_details

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
