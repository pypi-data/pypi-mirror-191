from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfirmationofpayeeJsonSrdAccount")


@attr.s(auto_attribs=True)
class ConfirmationofpayeeJsonSrdAccount:
    """List of responses on the current page

    Attributes:
        sort_code (str): The sort code of one or more accounts that requires Secondary Reference Data to be provided
            when making account name check requests.
             Example: 123456.
        account_numbers (Union[Unset, List[str]]): Account numbers that require Secondary Reference Data. If empty,
            Secondary Reference Data is required for all name check requests for this sort code. Example: ['11111111',
            '22222222'].
    """

    sort_code: str
    account_numbers: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sort_code = self.sort_code
        account_numbers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.account_numbers, Unset):
            account_numbers = self.account_numbers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sortCode": sort_code,
            }
        )
        if account_numbers is not UNSET:
            field_dict["accountNumbers"] = account_numbers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sort_code = d.pop("sortCode")

        account_numbers = cast(List[str], d.pop("accountNumbers", UNSET))

        confirmationofpayee_json_srd_account = cls(
            sort_code=sort_code,
            account_numbers=account_numbers,
        )

        confirmationofpayee_json_srd_account.additional_properties = d
        return confirmationofpayee_json_srd_account

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
