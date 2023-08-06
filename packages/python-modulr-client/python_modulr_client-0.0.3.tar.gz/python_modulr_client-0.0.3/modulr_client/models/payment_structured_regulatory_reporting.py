from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentStructuredRegulatoryReporting")


@attr.s(auto_attribs=True)
class PaymentStructuredRegulatoryReporting:
    """Structured regulatory reporting

    Attributes:
        amount (Union[Unset, float]): Amount of the payment in Major Current Units - '1' = 1.00 GBP Example: 100.
        code (Union[Unset, str]):
        currency_code (Union[Unset, str]): Currency of the account in ISO 4217 format. Default is GBP Example: GBP.
        information (Union[Unset, str]):
    """

    amount: Union[Unset, float] = UNSET
    code: Union[Unset, str] = UNSET
    currency_code: Union[Unset, str] = UNSET
    information: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        code = self.code
        currency_code = self.currency_code
        information = self.information

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if code is not UNSET:
            field_dict["code"] = code
        if currency_code is not UNSET:
            field_dict["currencyCode"] = currency_code
        if information is not UNSET:
            field_dict["information"] = information

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        code = d.pop("code", UNSET)

        currency_code = d.pop("currencyCode", UNSET)

        information = d.pop("information", UNSET)

        payment_structured_regulatory_reporting = cls(
            amount=amount,
            code=code,
            currency_code=currency_code,
            information=information,
        )

        payment_structured_regulatory_reporting.additional_properties = d
        return payment_structured_regulatory_reporting

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
