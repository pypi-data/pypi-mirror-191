from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_update_card_holder import CardUpdateCardHolder


T = TypeVar("T", bound="CardUpdateCardRequest")


@attr.s(auto_attribs=True)
class CardUpdateCardRequest:
    """Update card

    Attributes:
        holder (Union[Unset, CardUpdateCardHolder]): CardHolder
        limit (Union[Unset, float]): Total card authorisation limit. Example: 1000.
    """

    holder: Union[Unset, "CardUpdateCardHolder"] = UNSET
    limit: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        holder: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.holder, Unset):
            holder = self.holder.to_dict()

        limit = self.limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if holder is not UNSET:
            field_dict["holder"] = holder
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_update_card_holder import CardUpdateCardHolder

        d = src_dict.copy()
        _holder = d.pop("holder", UNSET)
        holder: Union[Unset, CardUpdateCardHolder]
        if isinstance(_holder, Unset):
            holder = UNSET
        else:
            holder = CardUpdateCardHolder.from_dict(_holder)

        limit = d.pop("limit", UNSET)

        card_update_card_request = cls(
            holder=holder,
            limit=limit,
        )

        card_update_card_request.additional_properties = d
        return card_update_card_request

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
