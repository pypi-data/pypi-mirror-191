from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.payment_charge_bearer import PaymentChargeBearer
from ..models.payment_charge_currency import PaymentChargeCurrency

T = TypeVar("T", bound="PaymentCharge")


@attr.s(auto_attribs=True)
class PaymentCharge:
    """
    Attributes:
        amount (float): Amount of the charges. Max allowed is 999999999999.99 Example: 100.
        bearer (PaymentChargeBearer): Information about bearer of the charges. Its can be Creditor, Debtor or shared
            between both Example: CRED.
        currency (PaymentChargeCurrency): Currency of charge. Should be ISO Standard currency Example: GBP.
    """

    amount: float
    bearer: PaymentChargeBearer
    currency: PaymentChargeCurrency
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        bearer = self.bearer.value

        currency = self.currency.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "bearer": bearer,
                "currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount")

        bearer = PaymentChargeBearer(d.pop("bearer"))

        currency = PaymentChargeCurrency(d.pop("currency"))

        payment_charge = cls(
            amount=amount,
            bearer=bearer,
            currency=currency,
        )

        payment_charge.additional_properties = d
        return payment_charge

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
