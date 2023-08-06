from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_identifier_response_type import AccountIdentifierResponseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_identifier_country_specific_details_response import (
        AccountIdentifierCountrySpecificDetailsResponse,
    )


T = TypeVar("T", bound="AccountIdentifierResponse")


@attr.s(auto_attribs=True)
class AccountIdentifierResponse:
    """Account Identifier

    Attributes:
        account_number (Union[Unset, str]): Bank account Sort Code Example: 12345678.
        bic (Union[Unset, str]):  Example: MODRGB21.
        country_specific_details (Union[Unset, AccountIdentifierCountrySpecificDetailsResponse]):  Example:
            {'branchCode': '123456789'}.
        currency (Union[Unset, str]):  Example: GBP.
        iban (Union[Unset, str]):  Example: GB20MODR04001401100000.
        sort_code (Union[Unset, str]): Bank account Sort Code Example: 000000.
        type (Union[Unset, AccountIdentifierResponseType]):
    """

    account_number: Union[Unset, str] = UNSET
    bic: Union[Unset, str] = UNSET
    country_specific_details: Union[
        Unset, "AccountIdentifierCountrySpecificDetailsResponse"
    ] = UNSET
    currency: Union[Unset, str] = UNSET
    iban: Union[Unset, str] = UNSET
    sort_code: Union[Unset, str] = UNSET
    type: Union[Unset, AccountIdentifierResponseType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_number = self.account_number
        bic = self.bic
        country_specific_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.country_specific_details, Unset):
            country_specific_details = self.country_specific_details.to_dict()

        currency = self.currency
        iban = self.iban
        sort_code = self.sort_code
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if bic is not UNSET:
            field_dict["bic"] = bic
        if country_specific_details is not UNSET:
            field_dict["countrySpecificDetails"] = country_specific_details
        if currency is not UNSET:
            field_dict["currency"] = currency
        if iban is not UNSET:
            field_dict["iban"] = iban
        if sort_code is not UNSET:
            field_dict["sortCode"] = sort_code
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_identifier_country_specific_details_response import (
            AccountIdentifierCountrySpecificDetailsResponse,
        )

        d = src_dict.copy()
        account_number = d.pop("accountNumber", UNSET)

        bic = d.pop("bic", UNSET)

        _country_specific_details = d.pop("countrySpecificDetails", UNSET)
        country_specific_details: Union[Unset, AccountIdentifierCountrySpecificDetailsResponse]
        if isinstance(_country_specific_details, Unset):
            country_specific_details = UNSET
        else:
            country_specific_details = AccountIdentifierCountrySpecificDetailsResponse.from_dict(
                _country_specific_details
            )

        currency = d.pop("currency", UNSET)

        iban = d.pop("iban", UNSET)

        sort_code = d.pop("sortCode", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, AccountIdentifierResponseType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AccountIdentifierResponseType(_type)

        account_identifier_response = cls(
            account_number=account_number,
            bic=bic,
            country_specific_details=country_specific_details,
            currency=currency,
            iban=iban,
            sort_code=sort_code,
            type=type,
        )

        account_identifier_response.additional_properties = d
        return account_identifier_response

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
