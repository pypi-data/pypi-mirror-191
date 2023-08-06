from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pispgateway_delivery_address_country import (
    PispgatewayDeliveryAddressCountry,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayDeliveryAddress")


@attr.s(auto_attribs=True)
class PispgatewayDeliveryAddress:
    """Information that locates and identifies a specific address, as defined by postal services or in free format text,
    must be specified if paymentContextCode is ECOMMERCEGOODS

        Attributes:
            address_line_1 (str): First line of the address
            country (PispgatewayDeliveryAddressCountry): The country
            post_code (str): The postcode
            post_town (str): The post town
            address_line_2 (Union[Unset, str]): Second line of the address
    """

    address_line_1: str
    country: PispgatewayDeliveryAddressCountry
    post_code: str
    post_town: str
    address_line_2: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address_line_1 = self.address_line_1
        country = self.country.value

        post_code = self.post_code
        post_town = self.post_town
        address_line_2 = self.address_line_2

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address_line_1 = d.pop("addressLine1")

        country = PispgatewayDeliveryAddressCountry(d.pop("country"))

        post_code = d.pop("postCode")

        post_town = d.pop("postTown")

        address_line_2 = d.pop("addressLine2", UNSET)

        pispgateway_delivery_address = cls(
            address_line_1=address_line_1,
            country=country,
            post_code=post_code,
            post_town=post_town,
            address_line_2=address_line_2,
        )

        pispgateway_delivery_address.additional_properties = d
        return pispgateway_delivery_address

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
