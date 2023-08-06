from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pispgateway_standing_order_payment import (
        PispgatewayStandingOrderPayment,
    )
    from ..models.pispgateway_standing_order_schedule import (
        PispgatewayStandingOrderSchedule,
    )


T = TypeVar("T", bound="PispgatewayGetStandingOrderInitiationResponse")


@attr.s(auto_attribs=True)
class PispgatewayGetStandingOrderInitiationResponse:
    """Response object for Get Standing Order Initiation

    Attributes:
        aspsp_id (Union[Unset, str]): The identifier of the ASPSP used for the standing order Example: H100000001.
        id (Union[Unset, str]): The identifier of the standing order initiation Example: I000000001.
        payment (Union[Unset, PispgatewayStandingOrderPayment]): The payment of the standing order
        schedule (Union[Unset, PispgatewayStandingOrderSchedule]): The schedule of the standing order
        standing_order_status (Union[Unset, str]): The status of the standing order at the ASPSP. When available, this
            is passed through from the ASPSP without modification. Example: InitiationCompleted.
        status (Union[Unset, str]): The status of the standing order initiation, can be one of SUBMITTED,
            AWAITING_CONSENT, CONSENT_REJECTED, EXECUTED, ER_EXPIRED, ER_EXTSYS, ER_GENERAL Example: AWAITING_CONSENT.
    """

    aspsp_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    payment: Union[Unset, "PispgatewayStandingOrderPayment"] = UNSET
    schedule: Union[Unset, "PispgatewayStandingOrderSchedule"] = UNSET
    standing_order_status: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspsp_id = self.aspsp_id
        id = self.id
        payment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payment, Unset):
            payment = self.payment.to_dict()

        schedule: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        standing_order_status = self.standing_order_status
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspsp_id is not UNSET:
            field_dict["aspspId"] = aspsp_id
        if id is not UNSET:
            field_dict["id"] = id
        if payment is not UNSET:
            field_dict["payment"] = payment
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if standing_order_status is not UNSET:
            field_dict["standingOrderStatus"] = standing_order_status
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_standing_order_payment import (
            PispgatewayStandingOrderPayment,
        )
        from ..models.pispgateway_standing_order_schedule import (
            PispgatewayStandingOrderSchedule,
        )

        d = src_dict.copy()
        aspsp_id = d.pop("aspspId", UNSET)

        id = d.pop("id", UNSET)

        _payment = d.pop("payment", UNSET)
        payment: Union[Unset, PispgatewayStandingOrderPayment]
        if isinstance(_payment, Unset):
            payment = UNSET
        else:
            payment = PispgatewayStandingOrderPayment.from_dict(_payment)

        _schedule = d.pop("schedule", UNSET)
        schedule: Union[Unset, PispgatewayStandingOrderSchedule]
        if isinstance(_schedule, Unset):
            schedule = UNSET
        else:
            schedule = PispgatewayStandingOrderSchedule.from_dict(_schedule)

        standing_order_status = d.pop("standingOrderStatus", UNSET)

        status = d.pop("status", UNSET)

        pispgateway_get_standing_order_initiation_response = cls(
            aspsp_id=aspsp_id,
            id=id,
            payment=payment,
            schedule=schedule,
            standing_order_status=standing_order_status,
            status=status,
        )

        pispgateway_get_standing_order_initiation_response.additional_properties = d
        return pispgateway_get_standing_order_initiation_response

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
