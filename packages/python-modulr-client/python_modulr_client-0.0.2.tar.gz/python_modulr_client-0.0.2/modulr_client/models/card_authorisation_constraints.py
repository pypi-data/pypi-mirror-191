from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_spend_constraint_detail import CardSpendConstraintDetail


T = TypeVar("T", bound="CardAuthorisationConstraints")


@attr.s(auto_attribs=True)
class CardAuthorisationConstraints:
    """Authorisation constraints

    Attributes:
        spend (Union[Unset, List['CardSpendConstraintDetail']]): Spending constraints
    """

    spend: Union[Unset, List["CardSpendConstraintDetail"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        spend: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.spend, Unset):
            spend = []
            for spend_item_data in self.spend:
                spend_item = spend_item_data.to_dict()

                spend.append(spend_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if spend is not UNSET:
            field_dict["spend"] = spend

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_spend_constraint_detail import CardSpendConstraintDetail

        d = src_dict.copy()
        spend = []
        _spend = d.pop("spend", UNSET)
        for spend_item_data in _spend or []:
            spend_item = CardSpendConstraintDetail.from_dict(spend_item_data)

            spend.append(spend_item)

        card_authorisation_constraints = cls(
            spend=spend,
        )

        card_authorisation_constraints.additional_properties = d
        return card_authorisation_constraints

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
