import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentBatchPaymentApproval")


@attr.s(auto_attribs=True)
class PaymentBatchPaymentApproval:
    """A single approval against a batch payment request

    Attributes:
        approved_by (Union[Unset, str]): ID of user who approved this batch payment request Example: U2100021.
        approved_on (Union[Unset, datetime.date]): Date this approval was applied Example: 2022-06-25.
    """

    approved_by: Union[Unset, str] = UNSET
    approved_on: Union[Unset, datetime.date] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approved_by = self.approved_by
        approved_on: Union[Unset, str] = UNSET
        if not isinstance(self.approved_on, Unset):
            approved_on = self.approved_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approved_by is not UNSET:
            field_dict["approvedBy"] = approved_by
        if approved_on is not UNSET:
            field_dict["approvedOn"] = approved_on

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        approved_by = d.pop("approvedBy", UNSET)

        _approved_on = d.pop("approvedOn", UNSET)
        approved_on: Union[Unset, datetime.date]
        if isinstance(_approved_on, Unset):
            approved_on = UNSET
        else:
            approved_on = isoparse(_approved_on).date()

        payment_batch_payment_approval = cls(
            approved_by=approved_by,
            approved_on=approved_on,
        )

        payment_batch_payment_approval.additional_properties = d
        return payment_batch_payment_approval

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
