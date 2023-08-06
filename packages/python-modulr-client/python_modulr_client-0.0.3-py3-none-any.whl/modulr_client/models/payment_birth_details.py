from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentBirthDetails")


@attr.s(auto_attribs=True)
class PaymentBirthDetails:
    """Birth details of a person. Official identification details. Property 'birthDetails' and/or 'officialIdentification'
    Or 'officialIdDetailOrgs' is mandatory

        Attributes:
            city_of_birth (Union[Unset, str]): City of birth of the ultimate payer Example: Edinburgh.
            country_of_birth (Union[Unset, str]): ISO 3166 country code of the ultimate payers country of birth Example: GB.
            date_of_birth (Union[Unset, str]): Date of birth in ISO 8601 format of the ultimate payer Example: 1978-01-01.
    """

    city_of_birth: Union[Unset, str] = UNSET
    country_of_birth: Union[Unset, str] = UNSET
    date_of_birth: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        city_of_birth = self.city_of_birth
        country_of_birth = self.country_of_birth
        date_of_birth = self.date_of_birth

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if city_of_birth is not UNSET:
            field_dict["cityOfBirth"] = city_of_birth
        if country_of_birth is not UNSET:
            field_dict["countryOfBirth"] = country_of_birth
        if date_of_birth is not UNSET:
            field_dict["dateOfBirth"] = date_of_birth

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        city_of_birth = d.pop("cityOfBirth", UNSET)

        country_of_birth = d.pop("countryOfBirth", UNSET)

        date_of_birth = d.pop("dateOfBirth", UNSET)

        payment_birth_details = cls(
            city_of_birth=city_of_birth,
            country_of_birth=country_of_birth,
            date_of_birth=date_of_birth,
        )

        payment_birth_details.additional_properties = d
        return payment_birth_details

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
