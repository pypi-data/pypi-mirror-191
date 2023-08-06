from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.account_access_group_with_details_response_status import (
    AccountAccessGroupWithDetailsResponseStatus,
)
from ..models.account_access_group_with_details_response_type import (
    AccountAccessGroupWithDetailsResponseType,
)

T = TypeVar("T", bound="AccountAccessGroupWithDetailsResponse")


@attr.s(auto_attribs=True)
class AccountAccessGroupWithDetailsResponse:
    """AccessGroupWithDetails

    Attributes:
        account_ids (List[str]): BIDs of Accounts in the group
        beneficiary_ids (List[str]): BIDs of Beneficiaries in the group
        count_of_accounts (int): The number of accounts in this group
        id (str): Unique ID for the access group Example: G0000001.
        name (str): Access group name
        status (AccountAccessGroupWithDetailsResponseStatus): Status of the access group
        type (AccountAccessGroupWithDetailsResponseType): The type of access group
        type_id (str): The identifier of the linked entity implied by the type, e.g. the partner ID
    """

    account_ids: List[str]
    beneficiary_ids: List[str]
    count_of_accounts: int
    id: str
    name: str
    status: AccountAccessGroupWithDetailsResponseStatus
    type: AccountAccessGroupWithDetailsResponseType
    type_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_ids = self.account_ids

        beneficiary_ids = self.beneficiary_ids

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
                "accountIds": account_ids,
                "beneficiaryIds": beneficiary_ids,
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
        account_ids = cast(List[str], d.pop("accountIds"))

        beneficiary_ids = cast(List[str], d.pop("beneficiaryIds"))

        count_of_accounts = d.pop("countOfAccounts")

        id = d.pop("id")

        name = d.pop("name")

        status = AccountAccessGroupWithDetailsResponseStatus(d.pop("status"))

        type = AccountAccessGroupWithDetailsResponseType(d.pop("type"))

        type_id = d.pop("typeId")

        account_access_group_with_details_response = cls(
            account_ids=account_ids,
            beneficiary_ids=beneficiary_ids,
            count_of_accounts=count_of_accounts,
            id=id,
            name=name,
            status=status,
            type=type,
            type_id=type_id,
        )

        account_access_group_with_details_response.additional_properties = d
        return account_access_group_with_details_response

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
