from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.directdebit_cancel_mandate_request_reason import (
    DirectdebitCancelMandateRequestReason,
)

T = TypeVar("T", bound="DirectdebitCancelMandateRequest")


@attr.s(auto_attribs=True)
class DirectdebitCancelMandateRequest:
    """Details of Mandate cancellation.

    Attributes:
        reason (DirectdebitCancelMandateRequestReason): Reason to cancel the mandate
    """

    reason: DirectdebitCancelMandateRequestReason
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = DirectdebitCancelMandateRequestReason(d.pop("reason"))

        directdebit_cancel_mandate_request = cls(
            reason=reason,
        )

        directdebit_cancel_mandate_request.additional_properties = d
        return directdebit_cancel_mandate_request

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
