from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pispgateway_payment_context_payment_context_code import (
    PispgatewayPaymentContextPaymentContextCode,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pispgateway_delivery_address import PispgatewayDeliveryAddress
    from ..models.pispgateway_merchant_details import PispgatewayMerchantDetails


T = TypeVar("T", bound="PispgatewayPaymentContext")


@attr.s(auto_attribs=True)
class PispgatewayPaymentContext:
    """Payment context for the initiation request

    Attributes:
        merchant (PispgatewayMerchantDetails): Merchant details for the payment context
        payment_context_code (PispgatewayPaymentContextPaymentContextCode): Indicates type of Payment Context, can be
            one of BILLPAYMENT, ECOMMERCEGOODS, ECOMMERCESERVICES, OTHER, PARTYTOPARTY
        delivery_address (Union[Unset, PispgatewayDeliveryAddress]): Information that locates and identifies a specific
            address, as defined by postal services or in free format text, must be specified if paymentContextCode is
            ECOMMERCEGOODS
    """

    merchant: "PispgatewayMerchantDetails"
    payment_context_code: PispgatewayPaymentContextPaymentContextCode
    delivery_address: Union[Unset, "PispgatewayDeliveryAddress"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        merchant = self.merchant.to_dict()

        payment_context_code = self.payment_context_code.value

        delivery_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_address, Unset):
            delivery_address = self.delivery_address.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "merchant": merchant,
                "paymentContextCode": payment_context_code,
            }
        )
        if delivery_address is not UNSET:
            field_dict["deliveryAddress"] = delivery_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_delivery_address import PispgatewayDeliveryAddress
        from ..models.pispgateway_merchant_details import PispgatewayMerchantDetails

        d = src_dict.copy()
        merchant = PispgatewayMerchantDetails.from_dict(d.pop("merchant"))

        payment_context_code = PispgatewayPaymentContextPaymentContextCode(
            d.pop("paymentContextCode")
        )

        _delivery_address = d.pop("deliveryAddress", UNSET)
        delivery_address: Union[Unset, PispgatewayDeliveryAddress]
        if isinstance(_delivery_address, Unset):
            delivery_address = UNSET
        else:
            delivery_address = PispgatewayDeliveryAddress.from_dict(_delivery_address)

        pispgateway_payment_context = cls(
            merchant=merchant,
            payment_context_code=payment_context_code,
            delivery_address=delivery_address,
        )

        pispgateway_payment_context.additional_properties = d
        return pispgateway_payment_context

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
