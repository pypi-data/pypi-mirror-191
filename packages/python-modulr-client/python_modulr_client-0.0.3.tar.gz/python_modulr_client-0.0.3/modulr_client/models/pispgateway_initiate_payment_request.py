from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pispgateway_destination import PispgatewayDestination
    from ..models.pispgateway_legacy_payment_context import (
        PispgatewayLegacyPaymentContext,
    )
    from ..models.pispgateway_payment_amount import PispgatewayPaymentAmount


T = TypeVar("T", bound="PispgatewayInitiatePaymentRequest")


@attr.s(auto_attribs=True)
class PispgatewayInitiatePaymentRequest:
    """Request object to Initiate Payment

    Attributes:
        aspsp_id (str): Identifier for ASPSP being used for the payment Example: H100000001.
        destination (PispgatewayDestination): The destination account for the payment
        payment_amount (PispgatewayPaymentAmount): The amount of the payment
        payment_reference (str): Reference to be used for the Payment. This will appear on the Account statement/the
            recipient's bank account. Min 6 to max 18 characters. Can contain alphanumeric, '-', '.', '&', '/' and space.
            Example: Invoice ABC123.
        payment_context (Union[Unset, PispgatewayLegacyPaymentContext]): Payment context for the initiation request
    """

    aspsp_id: str
    destination: "PispgatewayDestination"
    payment_amount: "PispgatewayPaymentAmount"
    payment_reference: str
    payment_context: Union[Unset, "PispgatewayLegacyPaymentContext"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspsp_id = self.aspsp_id
        destination = self.destination.to_dict()

        payment_amount = self.payment_amount.to_dict()

        payment_reference = self.payment_reference
        payment_context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payment_context, Unset):
            payment_context = self.payment_context.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aspspId": aspsp_id,
                "destination": destination,
                "paymentAmount": payment_amount,
                "paymentReference": payment_reference,
            }
        )
        if payment_context is not UNSET:
            field_dict["paymentContext"] = payment_context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_destination import PispgatewayDestination
        from ..models.pispgateway_legacy_payment_context import (
            PispgatewayLegacyPaymentContext,
        )
        from ..models.pispgateway_payment_amount import PispgatewayPaymentAmount

        d = src_dict.copy()
        aspsp_id = d.pop("aspspId")

        destination = PispgatewayDestination.from_dict(d.pop("destination"))

        payment_amount = PispgatewayPaymentAmount.from_dict(d.pop("paymentAmount"))

        payment_reference = d.pop("paymentReference")

        _payment_context = d.pop("paymentContext", UNSET)
        payment_context: Union[Unset, PispgatewayLegacyPaymentContext]
        if isinstance(_payment_context, Unset):
            payment_context = UNSET
        else:
            payment_context = PispgatewayLegacyPaymentContext.from_dict(_payment_context)

        pispgateway_initiate_payment_request = cls(
            aspsp_id=aspsp_id,
            destination=destination,
            payment_amount=payment_amount,
            payment_reference=payment_reference,
            payment_context=payment_context,
        )

        pispgateway_initiate_payment_request.additional_properties = d
        return pispgateway_initiate_payment_request

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
