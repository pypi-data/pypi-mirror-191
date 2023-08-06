from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pispgateway_destination import PispgatewayDestination
    from ..models.pispgateway_payment_amount import PispgatewayPaymentAmount


T = TypeVar("T", bound="PispgatewayGetPaymentInitiationResponse")


@attr.s(auto_attribs=True)
class PispgatewayGetPaymentInitiationResponse:
    """Response object for Get Payment Initiation

    Attributes:
        aspsp_id (Union[Unset, str]): The identifier of the ASPSP used for the payment Example: H100000001.
        aspsp_payment_status (Union[Unset, str]): The status of the payment at the ASPSP. When available, this is passed
            through from the ASPSP without modification. Example: AcceptedSettlementCompleted.
        destination (Union[Unset, PispgatewayDestination]): The destination account for the payment
        id (Union[Unset, str]): The identifier of the payment initiation Example: I000000001.
        payment_amount (Union[Unset, PispgatewayPaymentAmount]): The amount of the payment
        payment_reference (Union[Unset, str]): The payment reference
        status (Union[Unset, str]): The status of the payment initiation, can be one of SUBMITTED, AWAITING_CONSENT,
            CONSENT_REJECTED, EXECUTED, ER_EXPIRED, ER_EXTSYS, ER_GENERAL Example: AWAITING_CONSENT.
    """

    aspsp_id: Union[Unset, str] = UNSET
    aspsp_payment_status: Union[Unset, str] = UNSET
    destination: Union[Unset, "PispgatewayDestination"] = UNSET
    id: Union[Unset, str] = UNSET
    payment_amount: Union[Unset, "PispgatewayPaymentAmount"] = UNSET
    payment_reference: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspsp_id = self.aspsp_id
        aspsp_payment_status = self.aspsp_payment_status
        destination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.destination, Unset):
            destination = self.destination.to_dict()

        id = self.id
        payment_amount: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payment_amount, Unset):
            payment_amount = self.payment_amount.to_dict()

        payment_reference = self.payment_reference
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspsp_id is not UNSET:
            field_dict["aspspId"] = aspsp_id
        if aspsp_payment_status is not UNSET:
            field_dict["aspspPaymentStatus"] = aspsp_payment_status
        if destination is not UNSET:
            field_dict["destination"] = destination
        if id is not UNSET:
            field_dict["id"] = id
        if payment_amount is not UNSET:
            field_dict["paymentAmount"] = payment_amount
        if payment_reference is not UNSET:
            field_dict["paymentReference"] = payment_reference
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_destination import PispgatewayDestination
        from ..models.pispgateway_payment_amount import PispgatewayPaymentAmount

        d = src_dict.copy()
        aspsp_id = d.pop("aspspId", UNSET)

        aspsp_payment_status = d.pop("aspspPaymentStatus", UNSET)

        _destination = d.pop("destination", UNSET)
        destination: Union[Unset, PispgatewayDestination]
        if isinstance(_destination, Unset):
            destination = UNSET
        else:
            destination = PispgatewayDestination.from_dict(_destination)

        id = d.pop("id", UNSET)

        _payment_amount = d.pop("paymentAmount", UNSET)
        payment_amount: Union[Unset, PispgatewayPaymentAmount]
        if isinstance(_payment_amount, Unset):
            payment_amount = UNSET
        else:
            payment_amount = PispgatewayPaymentAmount.from_dict(_payment_amount)

        payment_reference = d.pop("paymentReference", UNSET)

        status = d.pop("status", UNSET)

        pispgateway_get_payment_initiation_response = cls(
            aspsp_id=aspsp_id,
            aspsp_payment_status=aspsp_payment_status,
            destination=destination,
            id=id,
            payment_amount=payment_amount,
            payment_reference=payment_reference,
            status=status,
        )

        pispgateway_get_payment_initiation_response.additional_properties = d
        return pispgateway_get_payment_initiation_response

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
