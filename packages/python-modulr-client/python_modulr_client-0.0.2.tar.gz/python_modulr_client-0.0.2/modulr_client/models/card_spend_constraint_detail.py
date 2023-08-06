from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.card_spend_constraint_detail_currency import (
    CardSpendConstraintDetailCurrency,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardSpendConstraintDetail")


@attr.s(auto_attribs=True)
class CardSpendConstraintDetail:
    """Spending constraints

    Attributes:
        currency (CardSpendConstraintDetailCurrency): A 3 letter ISO 4217 code representing the transaction currency
            Example: GBP.
        max_ (Union[Unset, float]): Maximum spend amount (inclusive) Example: 2000.
        min_ (Union[Unset, float]): Minimum spend amount (inclusive) Example: 5.
    """

    currency: CardSpendConstraintDetailCurrency
    max_: Union[Unset, float] = UNSET
    min_: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency = self.currency.value

        max_ = self.max_
        min_ = self.min_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currency": currency,
            }
        )
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency = CardSpendConstraintDetailCurrency(d.pop("currency"))

        max_ = d.pop("max", UNSET)

        min_ = d.pop("min", UNSET)

        card_spend_constraint_detail = cls(
            currency=currency,
            max_=max_,
            min_=min_,
        )

        card_spend_constraint_detail.additional_properties = d
        return card_spend_constraint_detail

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
