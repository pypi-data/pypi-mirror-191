from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardCardEnquiryRequest")


@attr.s(auto_attribs=True)
class CardCardEnquiryRequest:
    """Enquiry

    Attributes:
        pan (Union[Unset, str]): pan
        provider_supplied_id (Union[Unset, str]): providerSuppliedId
    """

    pan: Union[Unset, str] = UNSET
    provider_supplied_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pan = self.pan
        provider_supplied_id = self.provider_supplied_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pan is not UNSET:
            field_dict["pan"] = pan
        if provider_supplied_id is not UNSET:
            field_dict["providerSuppliedId"] = provider_supplied_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pan = d.pop("pan", UNSET)

        provider_supplied_id = d.pop("providerSuppliedId", UNSET)

        card_card_enquiry_request = cls(
            pan=pan,
            provider_supplied_id=provider_supplied_id,
        )

        card_card_enquiry_request.additional_properties = d
        return card_card_enquiry_request

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
