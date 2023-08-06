from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_update_associate_request_type import (
    AccountUpdateAssociateRequestType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_request import AccountAddressRequest


T = TypeVar("T", bound="AccountUpdateAssociateRequest")


@attr.s(auto_attribs=True)
class AccountUpdateAssociateRequest:
    """Applicable to all types except 'PCM_BUSINESS'

    Attributes:
        first_name (str): Letters, hyphens and apostrophes
        home_address (AccountAddressRequest): Applicable to all types except 'INDIVIDUAL' and 'PCM_INDIVIDUAL'
        last_name (str): Letters, hyphens and apostrophes
        type (AccountUpdateAssociateRequestType): Type of associate
        date_of_birth (Union[Unset, str]): Date in yyyy-MM-dd format. If associate is a non-applicant director or
            partner, then partial DOB of yyyy-MM format is allowed. Valid age is from 16 to 100 years. If Applicant then
            minimum age required is 18 years for specific partners. Required for all associate types except PCM_INDIVIDUAL.
        id (Union[Unset, str]): ID of associate
        middle_name (Union[Unset, str]): Letters, hyphens and apostrophes
        ownership (Union[Unset, int]): Ownership percentage for Partners
    """

    first_name: str
    home_address: "AccountAddressRequest"
    last_name: str
    type: AccountUpdateAssociateRequestType
    date_of_birth: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    ownership: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        home_address = self.home_address.to_dict()

        last_name = self.last_name
        type = self.type.value

        date_of_birth = self.date_of_birth
        id = self.id
        middle_name = self.middle_name
        ownership = self.ownership

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "firstName": first_name,
                "homeAddress": home_address,
                "lastName": last_name,
                "type": type,
            }
        )
        if date_of_birth is not UNSET:
            field_dict["dateOfBirth"] = date_of_birth
        if id is not UNSET:
            field_dict["id"] = id
        if middle_name is not UNSET:
            field_dict["middleName"] = middle_name
        if ownership is not UNSET:
            field_dict["ownership"] = ownership

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_address_request import AccountAddressRequest

        d = src_dict.copy()
        first_name = d.pop("firstName")

        home_address = AccountAddressRequest.from_dict(d.pop("homeAddress"))

        last_name = d.pop("lastName")

        type = AccountUpdateAssociateRequestType(d.pop("type"))

        date_of_birth = d.pop("dateOfBirth", UNSET)

        id = d.pop("id", UNSET)

        middle_name = d.pop("middleName", UNSET)

        ownership = d.pop("ownership", UNSET)

        account_update_associate_request = cls(
            first_name=first_name,
            home_address=home_address,
            last_name=last_name,
            type=type,
            date_of_birth=date_of_birth,
            id=id,
            middle_name=middle_name,
            ownership=ownership,
        )

        account_update_associate_request.additional_properties = d
        return account_update_associate_request

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
