import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_response import AccountAddressResponse


T = TypeVar("T", bound="AccountDelegateResponse")


@attr.s(auto_attribs=True)
class AccountDelegateResponse:
    """Delegate

    Attributes:
        created (datetime.datetime): Datetime the Delegate was created.Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC
            offset. e.g 2017-01-28T01:01:01+0000
        id (str): Unique reference for the Delegate. Example: D0000001.
        name (str): Name for the Delegate
        role_id (str): The id of the Role assigned to the delegate Example: R02002M5.
        status (str): Status of the Delegate.
        updated (datetime.datetime): Datetime the Delegate was last updated.Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z
            is UTC offset. e.g 2017-01-28T01:01:01+0000
        address (Union[Unset, AccountAddressResponse]): Address
        external_reference (Union[Unset, str]): External system reference for the Delegate
        partner (Union[Unset, str]): Partner Bid. Example: R0000001.
    """

    created: datetime.datetime
    id: str
    name: str
    role_id: str
    status: str
    updated: datetime.datetime
    address: Union[Unset, "AccountAddressResponse"] = UNSET
    external_reference: Union[Unset, str] = UNSET
    partner: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created = self.created.isoformat()

        id = self.id
        name = self.name
        role_id = self.role_id
        status = self.status
        updated = self.updated.isoformat()

        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        external_reference = self.external_reference
        partner = self.partner

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "id": id,
                "name": name,
                "roleId": role_id,
                "status": status,
                "updated": updated,
            }
        )
        if address is not UNSET:
            field_dict["address"] = address
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if partner is not UNSET:
            field_dict["partner"] = partner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_address_response import AccountAddressResponse

        d = src_dict.copy()
        created = isoparse(d.pop("created"))

        id = d.pop("id")

        name = d.pop("name")

        role_id = d.pop("roleId")

        status = d.pop("status")

        updated = isoparse(d.pop("updated"))

        _address = d.pop("address", UNSET)
        address: Union[Unset, AccountAddressResponse]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = AccountAddressResponse.from_dict(_address)

        external_reference = d.pop("externalReference", UNSET)

        partner = d.pop("partner", UNSET)

        account_delegate_response = cls(
            created=created,
            id=id,
            name=name,
            role_id=role_id,
            status=status,
            updated=updated,
            address=address,
            external_reference=external_reference,
            partner=partner,
        )

        account_delegate_response.additional_properties = d
        return account_delegate_response

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
