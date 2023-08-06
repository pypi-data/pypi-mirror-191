from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.pispgateway_destination import PispgatewayDestination
    from ..models.pispgateway_standing_order_payment_amount import (
        PispgatewayStandingOrderPaymentAmount,
    )


T = TypeVar("T", bound="PispgatewayStandingOrderPayment")


@attr.s(auto_attribs=True)
class PispgatewayStandingOrderPayment:
    """The payment of the standing order

    Attributes:
        amount (PispgatewayStandingOrderPaymentAmount): The amount of the standing order
        destination (PispgatewayDestination): The destination account for the payment
        reference (str): Reference to be used for the Payment. This will appear on the Account statement/the recipient's
            bank account. Min 6 to max 18 characters. Can contain alphanumeric, '-', '.', '&', '/' and space. Example:
            Invoice ABC123.
    """

    amount: "PispgatewayStandingOrderPaymentAmount"
    destination: "PispgatewayDestination"
    reference: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount.to_dict()

        destination = self.destination.to_dict()

        reference = self.reference

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "destination": destination,
                "reference": reference,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_destination import PispgatewayDestination
        from ..models.pispgateway_standing_order_payment_amount import (
            PispgatewayStandingOrderPaymentAmount,
        )

        d = src_dict.copy()
        amount = PispgatewayStandingOrderPaymentAmount.from_dict(d.pop("amount"))

        destination = PispgatewayDestination.from_dict(d.pop("destination"))

        reference = d.pop("reference")

        pispgateway_standing_order_payment = cls(
            amount=amount,
            destination=destination,
            reference=reference,
        )

        pispgateway_standing_order_payment.additional_properties = d
        return pispgateway_standing_order_payment

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
