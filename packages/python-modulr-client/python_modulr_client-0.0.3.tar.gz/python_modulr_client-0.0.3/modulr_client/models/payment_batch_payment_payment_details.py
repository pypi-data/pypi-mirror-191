from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.payment_payments_summary import PaymentPaymentsSummary


T = TypeVar("T", bound="PaymentBatchPaymentPaymentDetails")


@attr.s(auto_attribs=True)
class PaymentBatchPaymentPaymentDetails:
    """Summary of payments and approvals, per currency (as a 3-alpha currency code)"""

    additional_properties: Dict[str, "PaymentPaymentsSummary"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_payments_summary import PaymentPaymentsSummary

        d = src_dict.copy()
        payment_batch_payment_payment_details = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PaymentPaymentsSummary.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        payment_batch_payment_payment_details.additional_properties = additional_properties
        return payment_batch_payment_payment_details

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "PaymentPaymentsSummary":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "PaymentPaymentsSummary") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
