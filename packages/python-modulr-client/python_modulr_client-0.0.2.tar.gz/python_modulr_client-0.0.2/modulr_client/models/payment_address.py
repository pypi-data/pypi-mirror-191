from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentAddress")


@attr.s(auto_attribs=True)
class PaymentAddress:
    """
    Attributes:
        country (str): ISO 3166 country code of the ultimate payers address Example: GB.
        address_line_1 (Union[Unset, str]): First line of the ultimate payers address Example: 2nd Floor.
        address_line_2 (Union[Unset, str]): Second line of the ultimate payers address Example: 123 High Street.
        post_code (Union[Unset, str]): Post code of the ultimate payers address Example: AB12 3XX.
        post_town (Union[Unset, str]): Postal town of the ultimate payers address Example: Edinburgh.
    """

    country: str
    address_line_1: Union[Unset, str] = UNSET
    address_line_2: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    post_town: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        country = self.country
        address_line_1 = self.address_line_1
        address_line_2 = self.address_line_2
        post_code = self.post_code
        post_town = self.post_town

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "country": country,
            }
        )
        if address_line_1 is not UNSET:
            field_dict["addressLine1"] = address_line_1
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if post_town is not UNSET:
            field_dict["postTown"] = post_town

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        country = d.pop("country")

        address_line_1 = d.pop("addressLine1", UNSET)

        address_line_2 = d.pop("addressLine2", UNSET)

        post_code = d.pop("postCode", UNSET)

        post_town = d.pop("postTown", UNSET)

        payment_address = cls(
            country=country,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            post_code=post_code,
            post_town=post_town,
        )

        payment_address.additional_properties = d
        return payment_address

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
