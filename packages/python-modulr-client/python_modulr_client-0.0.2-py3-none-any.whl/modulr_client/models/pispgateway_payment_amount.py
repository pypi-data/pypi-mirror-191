from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.pispgateway_payment_amount_currency import (
    PispgatewayPaymentAmountCurrency,
)

T = TypeVar("T", bound="PispgatewayPaymentAmount")


@attr.s(auto_attribs=True)
class PispgatewayPaymentAmount:
    """The amount of the payment

    Attributes:
        currency (PispgatewayPaymentAmountCurrency): Currency of the account in ISO 4217 format. Only allowable value is
            GBP
        value (float): Amount of the payment in Major Currency Units - '1' = 1.00 GBP Example: 100.
    """

    currency: PispgatewayPaymentAmountCurrency
    value: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency = self.currency.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currency": currency,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency = PispgatewayPaymentAmountCurrency(d.pop("currency"))

        value = d.pop("value")

        pispgateway_payment_amount = cls(
            currency=currency,
            value=value,
        )

        pispgateway_payment_amount.additional_properties = d
        return pispgateway_payment_amount

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
