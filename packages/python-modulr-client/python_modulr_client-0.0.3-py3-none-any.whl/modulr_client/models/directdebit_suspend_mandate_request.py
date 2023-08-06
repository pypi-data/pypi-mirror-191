from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DirectdebitSuspendMandateRequest")


@attr.s(auto_attribs=True)
class DirectdebitSuspendMandateRequest:
    """Details of Mandate suspension.

    Attributes:
        reason (str): Reason to suspend the mandate
        cancel_all_scheduled_payments (Union[Unset, bool]): Should cancel all collections schedules for the mandate
    """

    reason: str
    cancel_all_scheduled_payments: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason
        cancel_all_scheduled_payments = self.cancel_all_scheduled_payments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
            }
        )
        if cancel_all_scheduled_payments is not UNSET:
            field_dict["cancelAllScheduledPayments"] = cancel_all_scheduled_payments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = d.pop("reason")

        cancel_all_scheduled_payments = d.pop("cancelAllScheduledPayments", UNSET)

        directdebit_suspend_mandate_request = cls(
            reason=reason,
            cancel_all_scheduled_payments=cancel_all_scheduled_payments,
        )

        directdebit_suspend_mandate_request.additional_properties = d
        return directdebit_suspend_mandate_request

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
