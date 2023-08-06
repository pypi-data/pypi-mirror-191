from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.pispgateway_payment_context import PispgatewayPaymentContext
    from ..models.pispgateway_standing_order_payment import (
        PispgatewayStandingOrderPayment,
    )
    from ..models.pispgateway_standing_order_schedule import (
        PispgatewayStandingOrderSchedule,
    )


T = TypeVar("T", bound="PispgatewayInitiateStandingOrderRequest")


@attr.s(auto_attribs=True)
class PispgatewayInitiateStandingOrderRequest:
    """Request object to Initiate Standing Order

    Attributes:
        aspsp_id (str): Identifier for ASPSP being used for the standing order Example: H100000001.
        context (PispgatewayPaymentContext): Payment context for the initiation request
        payment (PispgatewayStandingOrderPayment): The payment of the standing order
        schedule (PispgatewayStandingOrderSchedule): The schedule of the standing order
    """

    aspsp_id: str
    context: "PispgatewayPaymentContext"
    payment: "PispgatewayStandingOrderPayment"
    schedule: "PispgatewayStandingOrderSchedule"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspsp_id = self.aspsp_id
        context = self.context.to_dict()

        payment = self.payment.to_dict()

        schedule = self.schedule.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aspspId": aspsp_id,
                "context": context,
                "payment": payment,
                "schedule": schedule,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_payment_context import PispgatewayPaymentContext
        from ..models.pispgateway_standing_order_payment import (
            PispgatewayStandingOrderPayment,
        )
        from ..models.pispgateway_standing_order_schedule import (
            PispgatewayStandingOrderSchedule,
        )

        d = src_dict.copy()
        aspsp_id = d.pop("aspspId")

        context = PispgatewayPaymentContext.from_dict(d.pop("context"))

        payment = PispgatewayStandingOrderPayment.from_dict(d.pop("payment"))

        schedule = PispgatewayStandingOrderSchedule.from_dict(d.pop("schedule"))

        pispgateway_initiate_standing_order_request = cls(
            aspsp_id=aspsp_id,
            context=context,
            payment=payment,
            schedule=schedule,
        )

        pispgateway_initiate_standing_order_request.additional_properties = d
        return pispgateway_initiate_standing_order_request

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
