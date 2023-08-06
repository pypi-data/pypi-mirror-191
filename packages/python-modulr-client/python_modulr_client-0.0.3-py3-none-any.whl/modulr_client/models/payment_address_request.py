from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.payment_address_request_country import PaymentAddressRequestCountry
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentAddressRequest")


@attr.s(auto_attribs=True)
class PaymentAddressRequest:
    """Optional address. Mandatory if destination type is INTL

    Attributes:
        address_line_1 (str):
        post_town (str):
        address_line_2 (Union[Unset, str]):
        country (Union[Unset, PaymentAddressRequestCountry]):
        country_sub_division (Union[Unset, str]):
        post_code (Union[Unset, str]):
    """

    address_line_1: str
    post_town: str
    address_line_2: Union[Unset, str] = UNSET
    country: Union[Unset, PaymentAddressRequestCountry] = UNSET
    country_sub_division: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address_line_1 = self.address_line_1
        post_town = self.post_town
        address_line_2 = self.address_line_2
        country: Union[Unset, str] = UNSET
        if not isinstance(self.country, Unset):
            country = self.country.value

        country_sub_division = self.country_sub_division
        post_code = self.post_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "addressLine1": address_line_1,
                "postTown": post_town,
            }
        )
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if country is not UNSET:
            field_dict["country"] = country
        if country_sub_division is not UNSET:
            field_dict["countrySubDivision"] = country_sub_division
        if post_code is not UNSET:
            field_dict["postCode"] = post_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address_line_1 = d.pop("addressLine1")

        post_town = d.pop("postTown")

        address_line_2 = d.pop("addressLine2", UNSET)

        _country = d.pop("country", UNSET)
        country: Union[Unset, PaymentAddressRequestCountry]
        if isinstance(_country, Unset):
            country = UNSET
        else:
            country = PaymentAddressRequestCountry(_country)

        country_sub_division = d.pop("countrySubDivision", UNSET)

        post_code = d.pop("postCode", UNSET)

        payment_address_request = cls(
            address_line_1=address_line_1,
            post_town=post_town,
            address_line_2=address_line_2,
            country=country,
            country_sub_division=country_sub_division,
            post_code=post_code,
        )

        payment_address_request.additional_properties = d
        return payment_address_request

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
