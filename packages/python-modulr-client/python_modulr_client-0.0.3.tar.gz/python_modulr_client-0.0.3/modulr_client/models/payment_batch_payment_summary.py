from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentBatchPaymentSummary")


@attr.s(auto_attribs=True)
class PaymentBatchPaymentSummary:
    """Summary of the state of payment requests in this batch

    Attributes:
        completed (Union[Unset, int]): Count of completed payments
        errors (Union[Unset, int]): Count of failed payment requests
        info (Union[Unset, str]): Additional information or error message regarding this batch payment request
        inprogress (Union[Unset, int]): Count of payment requests in progress
        invalid (Union[Unset, int]): Count of invalid payment requests
        strict (Union[Unset, bool]):
        total (Union[Unset, int]): Total count of payment requests in this batch
    """

    completed: Union[Unset, int] = UNSET
    errors: Union[Unset, int] = UNSET
    info: Union[Unset, str] = UNSET
    inprogress: Union[Unset, int] = UNSET
    invalid: Union[Unset, int] = UNSET
    strict: Union[Unset, bool] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completed = self.completed
        errors = self.errors
        info = self.info
        inprogress = self.inprogress
        invalid = self.invalid
        strict = self.strict
        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if completed is not UNSET:
            field_dict["completed"] = completed
        if errors is not UNSET:
            field_dict["errors"] = errors
        if info is not UNSET:
            field_dict["info"] = info
        if inprogress is not UNSET:
            field_dict["inprogress"] = inprogress
        if invalid is not UNSET:
            field_dict["invalid"] = invalid
        if strict is not UNSET:
            field_dict["strict"] = strict
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed", UNSET)

        errors = d.pop("errors", UNSET)

        info = d.pop("info", UNSET)

        inprogress = d.pop("inprogress", UNSET)

        invalid = d.pop("invalid", UNSET)

        strict = d.pop("strict", UNSET)

        total = d.pop("total", UNSET)

        payment_batch_payment_summary = cls(
            completed=completed,
            errors=errors,
            info=info,
            inprogress=inprogress,
            invalid=invalid,
            strict=strict,
            total=total,
        )

        payment_batch_payment_summary.additional_properties = d
        return payment_batch_payment_summary

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
