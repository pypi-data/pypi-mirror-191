from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentPaymentsSummary")


@attr.s(auto_attribs=True)
class PaymentPaymentsSummary:
    """Summary of payments and approvals

    Attributes:
        pending_approval_amount (Union[Unset, float]): Sum total of payment amounts currently pending approval Example:
            50.
        pending_approval_count (Union[Unset, int]): Count of payments currently pending approval Example: 5.
        total_amount (Union[Unset, float]): Sum total of payment amounts Example: 100.
        total_payment_count (Union[Unset, int]): Total count of payments Example: 10.
    """

    pending_approval_amount: Union[Unset, float] = UNSET
    pending_approval_count: Union[Unset, int] = UNSET
    total_amount: Union[Unset, float] = UNSET
    total_payment_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pending_approval_amount = self.pending_approval_amount
        pending_approval_count = self.pending_approval_count
        total_amount = self.total_amount
        total_payment_count = self.total_payment_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pending_approval_amount is not UNSET:
            field_dict["pendingApprovalAmount"] = pending_approval_amount
        if pending_approval_count is not UNSET:
            field_dict["pendingApprovalCount"] = pending_approval_count
        if total_amount is not UNSET:
            field_dict["totalAmount"] = total_amount
        if total_payment_count is not UNSET:
            field_dict["totalPaymentCount"] = total_payment_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pending_approval_amount = d.pop("pendingApprovalAmount", UNSET)

        pending_approval_count = d.pop("pendingApprovalCount", UNSET)

        total_amount = d.pop("totalAmount", UNSET)

        total_payment_count = d.pop("totalPaymentCount", UNSET)

        payment_payments_summary = cls(
            pending_approval_amount=pending_approval_amount,
            pending_approval_count=pending_approval_count,
            total_amount=total_amount,
            total_payment_count=total_payment_count,
        )

        payment_payments_summary.additional_properties = d
        return payment_payments_summary

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
