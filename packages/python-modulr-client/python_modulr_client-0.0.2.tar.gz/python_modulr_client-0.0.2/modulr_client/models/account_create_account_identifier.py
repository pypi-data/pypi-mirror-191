from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.account_create_account_identifier_type import (
    AccountCreateAccountIdentifierType,
)

T = TypeVar("T", bound="AccountCreateAccountIdentifier")


@attr.s(auto_attribs=True)
class AccountCreateAccountIdentifier:
    """The identifier to assign to the account. Only available to selected partners.

    Attributes:
        account_number (str):
        sort_code (str):
        type (AccountCreateAccountIdentifierType):
    """

    account_number: str
    sort_code: str
    type: AccountCreateAccountIdentifierType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_number = self.account_number
        sort_code = self.sort_code
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountNumber": account_number,
                "sortCode": sort_code,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_number = d.pop("accountNumber")

        sort_code = d.pop("sortCode")

        type = AccountCreateAccountIdentifierType(d.pop("type"))

        account_create_account_identifier = cls(
            account_number=account_number,
            sort_code=sort_code,
            type=type,
        )

        account_create_account_identifier.additional_properties = d
        return account_create_account_identifier

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
