import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_request import AccountAddressRequest
    from ..models.account_identifier_request import AccountIdentifierRequest


T = TypeVar("T", bound="AccountCreateBeneficiaryRequest")


@attr.s(auto_attribs=True)
class AccountCreateBeneficiaryRequest:
    """
    Attributes:
        default_reference (str):
        destination_identifier (AccountIdentifierRequest):
        name (str):
        address (Union[Unset, AccountAddressRequest]): Applicable to all types except 'INDIVIDUAL' and 'PCM_INDIVIDUAL'
        birthdate (Union[Unset, datetime.date]): The destination beneficiary's date of birth. Date in yyyy-MM-dd format
        email_address (Union[Unset, str]): The destination beneficiary's email address
        external_reference (Union[Unset, str]): External Reference can only have alphanumeric characters plus
            underscore, hyphen and space up to 50 characters long
        id_to_replace (Union[Unset, str]):
        phone_number (Union[Unset, str]): The destination beneficiary's phone number, will be formatted into
            international number pattern
        qualifier (Union[Unset, str]): Optional qualifier. Only to be supplied if multiple beneficiaries with same
            destination need to be supplied
    """

    default_reference: str
    destination_identifier: "AccountIdentifierRequest"
    name: str
    address: Union[Unset, "AccountAddressRequest"] = UNSET
    birthdate: Union[Unset, datetime.date] = UNSET
    email_address: Union[Unset, str] = UNSET
    external_reference: Union[Unset, str] = UNSET
    id_to_replace: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    qualifier: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        default_reference = self.default_reference
        destination_identifier = self.destination_identifier.to_dict()

        name = self.name
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        birthdate: Union[Unset, str] = UNSET
        if not isinstance(self.birthdate, Unset):
            birthdate = self.birthdate.isoformat()

        email_address = self.email_address
        external_reference = self.external_reference
        id_to_replace = self.id_to_replace
        phone_number = self.phone_number
        qualifier = self.qualifier

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "defaultReference": default_reference,
                "destinationIdentifier": destination_identifier,
                "name": name,
            }
        )
        if address is not UNSET:
            field_dict["address"] = address
        if birthdate is not UNSET:
            field_dict["birthdate"] = birthdate
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if id_to_replace is not UNSET:
            field_dict["idToReplace"] = id_to_replace
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if qualifier is not UNSET:
            field_dict["qualifier"] = qualifier

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_address_request import AccountAddressRequest
        from ..models.account_identifier_request import AccountIdentifierRequest

        d = src_dict.copy()
        default_reference = d.pop("defaultReference")

        destination_identifier = AccountIdentifierRequest.from_dict(d.pop("destinationIdentifier"))

        name = d.pop("name")

        _address = d.pop("address", UNSET)
        address: Union[Unset, AccountAddressRequest]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = AccountAddressRequest.from_dict(_address)

        _birthdate = d.pop("birthdate", UNSET)
        birthdate: Union[Unset, datetime.date]
        if isinstance(_birthdate, Unset):
            birthdate = UNSET
        else:
            birthdate = isoparse(_birthdate).date()

        email_address = d.pop("emailAddress", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        id_to_replace = d.pop("idToReplace", UNSET)

        phone_number = d.pop("phoneNumber", UNSET)

        qualifier = d.pop("qualifier", UNSET)

        account_create_beneficiary_request = cls(
            default_reference=default_reference,
            destination_identifier=destination_identifier,
            name=name,
            address=address,
            birthdate=birthdate,
            email_address=email_address,
            external_reference=external_reference,
            id_to_replace=id_to_replace,
            phone_number=phone_number,
            qualifier=qualifier,
        )

        account_create_beneficiary_request.additional_properties = d
        return account_create_beneficiary_request

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
