from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="InboundpaymentAddress")


@attr.s(auto_attribs=True)
class InboundpaymentAddress:
    """Party address

    Attributes:
        address_line_1 (Union[Unset, str]):
        address_line_2 (Union[Unset, str]):
        country (Union[Unset, str]):
        post_code (Union[Unset, str]):
        post_town (Union[Unset, str]):
    """

    address_line_1: Union[Unset, str] = UNSET
    address_line_2: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    post_town: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address_line_1 = self.address_line_1
        address_line_2 = self.address_line_2
        country = self.country
        post_code = self.post_code
        post_town = self.post_town

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address_line_1 is not UNSET:
            field_dict["addressLine1"] = address_line_1
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if country is not UNSET:
            field_dict["country"] = country
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if post_town is not UNSET:
            field_dict["postTown"] = post_town

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address_line_1 = d.pop("addressLine1", UNSET)

        address_line_2 = d.pop("addressLine2", UNSET)

        country = d.pop("country", UNSET)

        post_code = d.pop("postCode", UNSET)

        post_town = d.pop("postTown", UNSET)

        inboundpayment_address = cls(
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            country=country,
            post_code=post_code,
            post_town=post_town,
        )

        inboundpayment_address.additional_properties = d
        return inboundpayment_address

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
