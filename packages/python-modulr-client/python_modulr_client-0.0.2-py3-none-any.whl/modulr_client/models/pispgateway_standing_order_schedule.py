from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pispgateway_standing_order_schedule_frequency import (
    PispgatewayStandingOrderScheduleFrequency,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayStandingOrderSchedule")


@attr.s(auto_attribs=True)
class PispgatewayStandingOrderSchedule:
    """The schedule of the standing order

    Attributes:
        frequency (PispgatewayStandingOrderScheduleFrequency): Type of the capability, can be one of WEEKLY, MONTHLY
        initial_date (str): The date on which the standing order should begin. This must be at least 3 days in the
            future from today. Date format 'yyyy-MM-dd' Example: 2021-03-25.
        final_date (Union[Unset, str]): The optional date on which the standing order should end. If unspecified, the
            standing order will continue until cancelled.This must be at least 3 days in the future from today. Date format
            'yyyy-MM-dd' Example: 2021-03-25.
    """

    frequency: PispgatewayStandingOrderScheduleFrequency
    initial_date: str
    final_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        frequency = self.frequency.value

        initial_date = self.initial_date
        final_date = self.final_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "frequency": frequency,
                "initialDate": initial_date,
            }
        )
        if final_date is not UNSET:
            field_dict["finalDate"] = final_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        frequency = PispgatewayStandingOrderScheduleFrequency(d.pop("frequency"))

        initial_date = d.pop("initialDate")

        final_date = d.pop("finalDate", UNSET)

        pispgateway_standing_order_schedule = cls(
            frequency=frequency,
            initial_date=initial_date,
            final_date=final_date,
        )

        pispgateway_standing_order_schedule.additional_properties = d
        return pispgateway_standing_order_schedule

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
