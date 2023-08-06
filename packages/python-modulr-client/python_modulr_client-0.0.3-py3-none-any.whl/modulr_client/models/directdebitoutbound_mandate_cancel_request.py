from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.directdebitoutbound_mandate_cancel_request_cancellation_code import (
    DirectdebitoutboundMandateCancelRequestCancellationCode,
)

T = TypeVar("T", bound="DirectdebitoutboundMandateCancelRequest")


@attr.s(auto_attribs=True)
class DirectdebitoutboundMandateCancelRequest:
    """Details of the Mandate Cancel Request

    Attributes:
        account_id (str): Account Id
        cancellation_code (DirectdebitoutboundMandateCancelRequestCancellationCode): Cancellation Code
        mandate_id (str): Mandate Id
        merchant_number (str): Merchant Number
    """

    account_id: str
    cancellation_code: DirectdebitoutboundMandateCancelRequestCancellationCode
    mandate_id: str
    merchant_number: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        cancellation_code = self.cancellation_code.value

        mandate_id = self.mandate_id
        merchant_number = self.merchant_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "cancellationCode": cancellation_code,
                "mandateId": mandate_id,
                "merchantNumber": merchant_number,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("accountId")

        cancellation_code = DirectdebitoutboundMandateCancelRequestCancellationCode(
            d.pop("cancellationCode")
        )

        mandate_id = d.pop("mandateId")

        merchant_number = d.pop("merchantNumber")

        directdebitoutbound_mandate_cancel_request = cls(
            account_id=account_id,
            cancellation_code=cancellation_code,
            mandate_id=mandate_id,
            merchant_number=merchant_number,
        )

        directdebitoutbound_mandate_cancel_request.additional_properties = d
        return directdebitoutbound_mandate_cancel_request

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
