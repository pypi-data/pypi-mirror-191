from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountAddressResponse")


@attr.s(auto_attribs=True)
class AccountAddressResponse:
    """Address

    Attributes:
        address_line_1 (str):
        country (str):
        post_code (str):
        post_town (str):
        address_line_2 (Union[Unset, str]):
        country_sub_division (Union[Unset, str]):
    """

    address_line_1: str
    country: str
    post_code: str
    post_town: str
    address_line_2: Union[Unset, str] = UNSET
    country_sub_division: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address_line_1 = self.address_line_1
        country = self.country
        post_code = self.post_code
        post_town = self.post_town
        address_line_2 = self.address_line_2
        country_sub_division = self.country_sub_division

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "addressLine1": address_line_1,
                "country": country,
                "postCode": post_code,
                "postTown": post_town,
            }
        )
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if country_sub_division is not UNSET:
            field_dict["countrySubDivision"] = country_sub_division

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address_line_1 = d.pop("addressLine1")

        country = d.pop("country")

        post_code = d.pop("postCode")

        post_town = d.pop("postTown")

        address_line_2 = d.pop("addressLine2", UNSET)

        country_sub_division = d.pop("countrySubDivision", UNSET)

        account_address_response = cls(
            address_line_1=address_line_1,
            country=country,
            post_code=post_code,
            post_town=post_town,
            address_line_2=address_line_2,
            country_sub_division=country_sub_division,
        )

        account_address_response.additional_properties = d
        return account_address_response

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
