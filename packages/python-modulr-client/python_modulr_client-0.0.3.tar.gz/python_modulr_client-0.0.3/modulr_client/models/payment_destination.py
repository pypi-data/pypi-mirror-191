import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.payment_destination_type import PaymentDestinationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_address_request import PaymentAddressRequest
    from ..models.payment_destination_country_specific_details import (
        PaymentDestinationCountrySpecificDetails,
    )


T = TypeVar("T", bound="PaymentDestination")


@attr.s(auto_attribs=True)
class PaymentDestination:
    """Destination of the Payment

    Attributes:
        type (PaymentDestinationType): Indicates the type of destination. Can be one of BENEFICIARY, ACCOUNT, SCAN, IBAN
            Example: SCAN.
        account_number (Union[Unset, str]): Account Number of destination account if using SCAN type. Example: 12345678.
        address (Union[Unset, PaymentAddressRequest]): Optional address. Mandatory if destination type is INTL
        bic (Union[Unset, str]): The destination beneficiary's BIC/Swift Code. Only to be used for INTL types.
        birthdate (Union[Unset, datetime.date]): The destination beneficiary's date of birth. Format: yyyy-MM-dd
            Example: 2000-01-01.
        country_specific_details (Union[Unset, PaymentDestinationCountrySpecificDetails]): Further details required,
            depending on the destination's country
        email_address (Union[Unset, str]): The destination beneficiary's email address
        iban (Union[Unset, str]): International Bank Account Number (IBAN). To be used as the destination identifier
            when sending ‘IBAN’ type payments Example: GB20MODR00000000000001.
        id (Union[Unset, str]): Identifier for the Payment destination if using ACCOUNT or BENEFICIARY type. Can be
            either: a) Beneficiary id for an external Payment, b) Account id for a transfer to another Account
        name (Union[Unset, str]): Name to use if a new beneficiary is created, and for using as the payee name if SCAN
            or IBAN types are specified for the destination Example: Test.
        phone_number (Union[Unset, str]): The destination beneficiary's phone number
        sort_code (Union[Unset, str]): Sort Code of destination account if using SCAN type. Example: 000000.
    """

    type: PaymentDestinationType
    account_number: Union[Unset, str] = UNSET
    address: Union[Unset, "PaymentAddressRequest"] = UNSET
    bic: Union[Unset, str] = UNSET
    birthdate: Union[Unset, datetime.date] = UNSET
    country_specific_details: Union[Unset, "PaymentDestinationCountrySpecificDetails"] = UNSET
    email_address: Union[Unset, str] = UNSET
    iban: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    sort_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        account_number = self.account_number
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        bic = self.bic
        birthdate: Union[Unset, str] = UNSET
        if not isinstance(self.birthdate, Unset):
            birthdate = self.birthdate.isoformat()

        country_specific_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.country_specific_details, Unset):
            country_specific_details = self.country_specific_details.to_dict()

        email_address = self.email_address
        iban = self.iban
        id = self.id
        name = self.name
        phone_number = self.phone_number
        sort_code = self.sort_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if address is not UNSET:
            field_dict["address"] = address
        if bic is not UNSET:
            field_dict["bic"] = bic
        if birthdate is not UNSET:
            field_dict["birthdate"] = birthdate
        if country_specific_details is not UNSET:
            field_dict["countrySpecificDetails"] = country_specific_details
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if iban is not UNSET:
            field_dict["iban"] = iban
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if sort_code is not UNSET:
            field_dict["sortCode"] = sort_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_address_request import PaymentAddressRequest
        from ..models.payment_destination_country_specific_details import (
            PaymentDestinationCountrySpecificDetails,
        )

        d = src_dict.copy()
        type = PaymentDestinationType(d.pop("type"))

        account_number = d.pop("accountNumber", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, PaymentAddressRequest]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = PaymentAddressRequest.from_dict(_address)

        bic = d.pop("bic", UNSET)

        _birthdate = d.pop("birthdate", UNSET)
        birthdate: Union[Unset, datetime.date]
        if isinstance(_birthdate, Unset):
            birthdate = UNSET
        else:
            birthdate = isoparse(_birthdate).date()

        _country_specific_details = d.pop("countrySpecificDetails", UNSET)
        country_specific_details: Union[Unset, PaymentDestinationCountrySpecificDetails]
        if isinstance(_country_specific_details, Unset):
            country_specific_details = UNSET
        else:
            country_specific_details = PaymentDestinationCountrySpecificDetails.from_dict(
                _country_specific_details
            )

        email_address = d.pop("emailAddress", UNSET)

        iban = d.pop("iban", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        phone_number = d.pop("phoneNumber", UNSET)

        sort_code = d.pop("sortCode", UNSET)

        payment_destination = cls(
            type=type,
            account_number=account_number,
            address=address,
            bic=bic,
            birthdate=birthdate,
            country_specific_details=country_specific_details,
            email_address=email_address,
            iban=iban,
            id=id,
            name=name,
            phone_number=phone_number,
            sort_code=sort_code,
        )

        payment_destination.additional_properties = d
        return payment_destination

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
