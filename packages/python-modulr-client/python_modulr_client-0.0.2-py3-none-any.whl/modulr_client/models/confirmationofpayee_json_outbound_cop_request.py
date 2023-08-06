from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.confirmationofpayee_json_outbound_cop_request_account_type import (
    ConfirmationofpayeeJsonOutboundCopRequestAccountType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfirmationofpayeeJsonOutboundCopRequest")


@attr.s(auto_attribs=True)
class ConfirmationofpayeeJsonOutboundCopRequest:
    """Details of Account Name Check Request

    Attributes:
        account_number (str): The account number. Example: 12345678.
        account_type (ConfirmationofpayeeJsonOutboundCopRequestAccountType): The type of account, either a personal or
            business account. Example: PERSONAL.
        name (str): The name to match the account name against. Example: Joe Bloggs.
        payment_account_id (str): The identifier of the account that a subsequent payment will be initiated from.
            Example: A123AAA4.
        sort_code (str): The sort code of the account. Example: 000000.
        secondary_account_id (Union[Unset, str]): Additional information used in conjunction with the Sort Code and
            Account Number to identify the account (such as a Building Society roll number). Example: A-1234567890.
    """

    account_number: str
    account_type: ConfirmationofpayeeJsonOutboundCopRequestAccountType
    name: str
    payment_account_id: str
    sort_code: str
    secondary_account_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_number = self.account_number
        account_type = self.account_type.value

        name = self.name
        payment_account_id = self.payment_account_id
        sort_code = self.sort_code
        secondary_account_id = self.secondary_account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountNumber": account_number,
                "accountType": account_type,
                "name": name,
                "paymentAccountId": payment_account_id,
                "sortCode": sort_code,
            }
        )
        if secondary_account_id is not UNSET:
            field_dict["secondaryAccountId"] = secondary_account_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_number = d.pop("accountNumber")

        account_type = ConfirmationofpayeeJsonOutboundCopRequestAccountType(d.pop("accountType"))

        name = d.pop("name")

        payment_account_id = d.pop("paymentAccountId")

        sort_code = d.pop("sortCode")

        secondary_account_id = d.pop("secondaryAccountId", UNSET)

        confirmationofpayee_json_outbound_cop_request = cls(
            account_number=account_number,
            account_type=account_type,
            name=name,
            payment_account_id=payment_account_id,
            sort_code=sort_code,
            secondary_account_id=secondary_account_id,
        )

        confirmationofpayee_json_outbound_cop_request.additional_properties = d
        return confirmationofpayee_json_outbound_cop_request

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
