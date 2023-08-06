from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.account_access_group_response_status import (
    AccountAccessGroupResponseStatus,
)
from ..models.account_access_group_response_type import AccountAccessGroupResponseType

T = TypeVar("T", bound="AccountAccessGroupResponse")


@attr.s(auto_attribs=True)
class AccountAccessGroupResponse:
    """AccessGroup

    Attributes:
        count_of_accounts (int): The number of accounts in this group
        id (str): Unique ID for the access group Example: G0000001.
        name (str): Access group name
        status (AccountAccessGroupResponseStatus): Status of the access group
        type (AccountAccessGroupResponseType): The type of access group
        type_id (str): The identifier of the linked entity implied by the type, e.g. the partner ID
    """

    count_of_accounts: int
    id: str
    name: str
    status: AccountAccessGroupResponseStatus
    type: AccountAccessGroupResponseType
    type_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count_of_accounts = self.count_of_accounts
        id = self.id
        name = self.name
        status = self.status.value

        type = self.type.value

        type_id = self.type_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "countOfAccounts": count_of_accounts,
                "id": id,
                "name": name,
                "status": status,
                "type": type,
                "typeId": type_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        count_of_accounts = d.pop("countOfAccounts")

        id = d.pop("id")

        name = d.pop("name")

        status = AccountAccessGroupResponseStatus(d.pop("status"))

        type = AccountAccessGroupResponseType(d.pop("type"))

        type_id = d.pop("typeId")

        account_access_group_response = cls(
            count_of_accounts=count_of_accounts,
            id=id,
            name=name,
            status=status,
            type=type,
            type_id=type_id,
        )

        account_access_group_response.additional_properties = d
        return account_access_group_response

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
