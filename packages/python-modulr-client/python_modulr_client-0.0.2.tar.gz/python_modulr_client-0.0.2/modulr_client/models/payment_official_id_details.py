from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentOfficialIdDetails")


@attr.s(auto_attribs=True)
class PaymentOfficialIdDetails:
    """Official identification for a person. Property 'birthDetails' and/or 'officialIdentification' Or
    'officialIdDetailOrgs' is mandatory

        Attributes:
            customer_number (Union[Unset, str]): Customer number Example: 23547326547632.
            driving_licence_number (Union[Unset, str]): Driving licence number Example: JONES849339TS8AD.
            id_card_number (Union[Unset, str]): National ID card number Example: 123456789.
            other_id_number (Union[Unset, str]): Other ID number Example: 123456789.
            passport_number (Union[Unset, str]): Passport number Example: 123456789.
            social_security_number (Union[Unset, str]): Social security number or equivalent Example: 1110000000022AB.
    """

    customer_number: Union[Unset, str] = UNSET
    driving_licence_number: Union[Unset, str] = UNSET
    id_card_number: Union[Unset, str] = UNSET
    other_id_number: Union[Unset, str] = UNSET
    passport_number: Union[Unset, str] = UNSET
    social_security_number: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        customer_number = self.customer_number
        driving_licence_number = self.driving_licence_number
        id_card_number = self.id_card_number
        other_id_number = self.other_id_number
        passport_number = self.passport_number
        social_security_number = self.social_security_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if customer_number is not UNSET:
            field_dict["customerNumber"] = customer_number
        if driving_licence_number is not UNSET:
            field_dict["drivingLicenceNumber"] = driving_licence_number
        if id_card_number is not UNSET:
            field_dict["idCardNumber"] = id_card_number
        if other_id_number is not UNSET:
            field_dict["otherIdNumber"] = other_id_number
        if passport_number is not UNSET:
            field_dict["passportNumber"] = passport_number
        if social_security_number is not UNSET:
            field_dict["socialSecurityNumber"] = social_security_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        customer_number = d.pop("customerNumber", UNSET)

        driving_licence_number = d.pop("drivingLicenceNumber", UNSET)

        id_card_number = d.pop("idCardNumber", UNSET)

        other_id_number = d.pop("otherIdNumber", UNSET)

        passport_number = d.pop("passportNumber", UNSET)

        social_security_number = d.pop("socialSecurityNumber", UNSET)

        payment_official_id_details = cls(
            customer_number=customer_number,
            driving_licence_number=driving_licence_number,
            id_card_number=id_card_number,
            other_id_number=other_id_number,
            passport_number=passport_number,
            social_security_number=social_security_number,
        )

        payment_official_id_details.additional_properties = d
        return payment_official_id_details

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
