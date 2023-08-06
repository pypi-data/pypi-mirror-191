import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_address_detail import CardAddressDetail


T = TypeVar("T", bound="CardCardHolder")


@attr.s(auto_attribs=True)
class CardCardHolder:
    """CardHolder

    Attributes:
        billing_address (CardAddressDetail): Address details for the cardholder. Optional for individual customers whose
            partner has verification type EXTERNAL.
        date_of_birth (datetime.date): Cardholder date of birth. Must match date format of yyyy-mm-dd. Required for
            virtual consumer and physical cards. Optional for individual customers. Example: 2001-01-01.
        first_name (str): Cardholder first name. Maximum of 20 alphanumeric characters including space, hyphen and
            apostrophe. Optional for individual customers whose partner has verification type EXTERNAL. Example: Joe.
        last_name (str): Cardholder last name. Maximum of 20 alphanumeric characters including space, hyphen and
            apostrophe. Optional for individual customers whose partner has verification type EXTERNAL. Example: Bloggs.
        mobile_number (str): Cardholder mobile number. Must start with a '+', followed by the country code and then the
            mobile number. Required for virtual consumer and physical cards. Example: +447123456000.
        email (Union[Unset, str]): Cardholder email Example: cardholder@example.com.
        title (Union[Unset, str]): Cardholder title is optional for all card types. Maximum of 4 alphanumeric
            characters. Example: Mr.
    """

    billing_address: "CardAddressDetail"
    date_of_birth: datetime.date
    first_name: str
    last_name: str
    mobile_number: str
    email: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        billing_address = self.billing_address.to_dict()

        date_of_birth = self.date_of_birth.isoformat()
        first_name = self.first_name
        last_name = self.last_name
        mobile_number = self.mobile_number
        email = self.email
        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "billingAddress": billing_address,
                "dateOfBirth": date_of_birth,
                "firstName": first_name,
                "lastName": last_name,
                "mobileNumber": mobile_number,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_address_detail import CardAddressDetail

        d = src_dict.copy()
        billing_address = CardAddressDetail.from_dict(d.pop("billingAddress"))

        date_of_birth = isoparse(d.pop("dateOfBirth")).date()

        first_name = d.pop("firstName")

        last_name = d.pop("lastName")

        mobile_number = d.pop("mobileNumber")

        email = d.pop("email", UNSET)

        title = d.pop("title", UNSET)

        card_card_holder = cls(
            billing_address=billing_address,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            email=email,
            title=title,
        )

        card_card_holder.additional_properties = d
        return card_card_holder

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
