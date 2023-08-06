from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.inboundpayment_account_identifier_detail_request_type import (
    InboundpaymentAccountIdentifierDetailRequestType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="InboundpaymentAccountIdentifierDetailRequest")


@attr.s(auto_attribs=True)
class InboundpaymentAccountIdentifierDetailRequest:
    """Account identifier

    Attributes:
        type (InboundpaymentAccountIdentifierDetailRequestType): Account identifier type
        account_number (Union[Unset, str]): Account number
        bic (Union[Unset, str]): BIC
        iban (Union[Unset, str]): IBAN
        sort_code (Union[Unset, str]): Sortcode
    """

    type: InboundpaymentAccountIdentifierDetailRequestType
    account_number: Union[Unset, str] = UNSET
    bic: Union[Unset, str] = UNSET
    iban: Union[Unset, str] = UNSET
    sort_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        account_number = self.account_number
        bic = self.bic
        iban = self.iban
        sort_code = self.sort_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if bic is not UNSET:
            field_dict["bic"] = bic
        if iban is not UNSET:
            field_dict["iban"] = iban
        if sort_code is not UNSET:
            field_dict["sortCode"] = sort_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = InboundpaymentAccountIdentifierDetailRequestType(d.pop("type"))

        account_number = d.pop("accountNumber", UNSET)

        bic = d.pop("bic", UNSET)

        iban = d.pop("iban", UNSET)

        sort_code = d.pop("sortCode", UNSET)

        inboundpayment_account_identifier_detail_request = cls(
            type=type,
            account_number=account_number,
            bic=bic,
            iban=iban,
            sort_code=sort_code,
        )

        inboundpayment_account_identifier_detail_request.additional_properties = d
        return inboundpayment_account_identifier_detail_request

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
