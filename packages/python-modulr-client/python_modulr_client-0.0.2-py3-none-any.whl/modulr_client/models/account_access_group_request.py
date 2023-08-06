from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.account_access_group_request_action import AccountAccessGroupRequestAction

T = TypeVar("T", bound="AccountAccessGroupRequest")


@attr.s(auto_attribs=True)
class AccountAccessGroupRequest:
    r"""
    Attributes:
        account_ids (List[str]): Bids of the accounts to be added/removed
        action (AccountAccessGroupRequestAction): Action to apply for the supplied account bid
        beneficiary_ids (List[str]): Bids of the beneficiaries to be added/removed
        name (str): The name of the account group to create. Must match: [\w \-]*
    """

    account_ids: List[str]
    action: AccountAccessGroupRequestAction
    beneficiary_ids: List[str]
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_ids = self.account_ids

        action = self.action.value

        beneficiary_ids = self.beneficiary_ids

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountIds": account_ids,
                "action": action,
                "beneficiaryIds": beneficiary_ids,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_ids = cast(List[str], d.pop("accountIds"))

        action = AccountAccessGroupRequestAction(d.pop("action"))

        beneficiary_ids = cast(List[str], d.pop("beneficiaryIds"))

        name = d.pop("name")

        account_access_group_request = cls(
            account_ids=account_ids,
            action=action,
            beneficiary_ids=beneficiary_ids,
            name=name,
        )

        account_access_group_request.additional_properties = d
        return account_access_group_request

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
