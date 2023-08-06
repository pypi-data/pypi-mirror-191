import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_address_detail import CardAddressDetail


T = TypeVar("T", bound="CardUpdateCardHolder")


@attr.s(auto_attribs=True)
class CardUpdateCardHolder:
    """CardHolder

    Attributes:
        billing_address (Union[Unset, CardAddressDetail]): Address details for the cardholder. Optional for individual
            customers whose partner has verification type EXTERNAL.
        date_of_birth (Union[Unset, datetime.date]): Cardholder date of birth. Must match date format of yyyy-mm-dd.
            Required for virtual consumer and physical cards. Must be NULL for individual customers. Example: 2001-01-01.
        email (Union[Unset, str]): Cardholder email Example: cardholder@example.com.
        mobile_number (Union[Unset, str]): Cardholder mobile number. Must start with a '+', followed by the country code
            and then the mobile number. Required for virtual consumer and physical cards. Example: +447123456000.
    """

    billing_address: Union[Unset, "CardAddressDetail"] = UNSET
    date_of_birth: Union[Unset, datetime.date] = UNSET
    email: Union[Unset, str] = UNSET
    mobile_number: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        billing_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.billing_address, Unset):
            billing_address = self.billing_address.to_dict()

        date_of_birth: Union[Unset, str] = UNSET
        if not isinstance(self.date_of_birth, Unset):
            date_of_birth = self.date_of_birth.isoformat()

        email = self.email
        mobile_number = self.mobile_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if billing_address is not UNSET:
            field_dict["billingAddress"] = billing_address
        if date_of_birth is not UNSET:
            field_dict["dateOfBirth"] = date_of_birth
        if email is not UNSET:
            field_dict["email"] = email
        if mobile_number is not UNSET:
            field_dict["mobileNumber"] = mobile_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_address_detail import CardAddressDetail

        d = src_dict.copy()
        _billing_address = d.pop("billingAddress", UNSET)
        billing_address: Union[Unset, CardAddressDetail]
        if isinstance(_billing_address, Unset):
            billing_address = UNSET
        else:
            billing_address = CardAddressDetail.from_dict(_billing_address)

        _date_of_birth = d.pop("dateOfBirth", UNSET)
        date_of_birth: Union[Unset, datetime.date]
        if isinstance(_date_of_birth, Unset):
            date_of_birth = UNSET
        else:
            date_of_birth = isoparse(_date_of_birth).date()

        email = d.pop("email", UNSET)

        mobile_number = d.pop("mobileNumber", UNSET)

        card_update_card_holder = cls(
            billing_address=billing_address,
            date_of_birth=date_of_birth,
            email=email,
            mobile_number=mobile_number,
        )

        card_update_card_holder.additional_properties = d
        return card_update_card_holder

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
