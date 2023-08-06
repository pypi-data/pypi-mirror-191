from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_payment_out_request import PaymentPaymentOutRequest


T = TypeVar("T", bound="PaymentBatchPaymentOutRequest")


@attr.s(auto_attribs=True)
class PaymentBatchPaymentOutRequest:
    """Details of Batch request

    Attributes:
        payments (List['PaymentPaymentOutRequest']): List of payments. Need at least 1 and maximum of 10000
        external_reference (Union[Unset, str]): Your reference for this Batch of payments Example: aReference_00001.
        strict_processing (Union[Unset, bool]): Flag to control if the entire batch fails for any individual payment
            validation failure
    """

    payments: List["PaymentPaymentOutRequest"]
    external_reference: Union[Unset, str] = UNSET
    strict_processing: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payments = []
        for payments_item_data in self.payments:
            payments_item = payments_item_data.to_dict()

            payments.append(payments_item)

        external_reference = self.external_reference
        strict_processing = self.strict_processing

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payments": payments,
            }
        )
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if strict_processing is not UNSET:
            field_dict["strictProcessing"] = strict_processing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_payment_out_request import PaymentPaymentOutRequest

        d = src_dict.copy()
        payments = []
        _payments = d.pop("payments")
        for payments_item_data in _payments:
            payments_item = PaymentPaymentOutRequest.from_dict(payments_item_data)

            payments.append(payments_item)

        external_reference = d.pop("externalReference", UNSET)

        strict_processing = d.pop("strictProcessing", UNSET)

        payment_batch_payment_out_request = cls(
            payments=payments,
            external_reference=external_reference,
            strict_processing=strict_processing,
        )

        payment_batch_payment_out_request.additional_properties = d
        return payment_batch_payment_out_request

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
