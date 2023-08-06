from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentfileuploadErrorMessageResponse")


@attr.s(auto_attribs=True)
class PaymentfileuploadErrorMessageResponse:
    """If invalid holds the validation errors

    Example:
        ['Failed parsing']

    Attributes:
        error_message (str): Error message indicating a certain validation error occurred Example: Processing date is
            required.
        invalid_accounts (Union[Unset, List[str]]): List of a invalid account that were effected by the validation
    """

    error_message: str
    invalid_accounts: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error_message = self.error_message
        invalid_accounts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.invalid_accounts, Unset):
            invalid_accounts = self.invalid_accounts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errorMessage": error_message,
            }
        )
        if invalid_accounts is not UNSET:
            field_dict["invalidAccounts"] = invalid_accounts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        error_message = d.pop("errorMessage")

        invalid_accounts = cast(List[str], d.pop("invalidAccounts", UNSET))

        paymentfileupload_error_message_response = cls(
            error_message=error_message,
            invalid_accounts=invalid_accounts,
        )

        paymentfileupload_error_message_response.additional_properties = d
        return paymentfileupload_error_message_response

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
