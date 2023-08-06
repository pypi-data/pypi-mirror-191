from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pispgateway_legacy_payment_context_payment_context_code import (
    PispgatewayLegacyPaymentContextPaymentContextCode,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pispgateway_delivery_address import PispgatewayDeliveryAddress


T = TypeVar("T", bound="PispgatewayLegacyPaymentContext")


@attr.s(auto_attribs=True)
class PispgatewayLegacyPaymentContext:
    """Payment context for the initiation request

    Attributes:
        payment_context_code (PispgatewayLegacyPaymentContextPaymentContextCode): Indicates type of Payment Context, can
            be one of BILLPAYMENT, ECOMMERCEGOODS, ECOMMERCESERVICES, OTHER, PARTYTOPARTY
        delivery_address (Union[Unset, PispgatewayDeliveryAddress]): Information that locates and identifies a specific
            address, as defined by postal services or in free format text, must be specified if paymentContextCode is
            ECOMMERCEGOODS
        merchant_category_code (Union[Unset, str]): Merchant category code conform to ISO 18245, related to the type of
            services or goods provided for the transaction. Must be specified if paymentContextCode is either ECOMMERCEGOODS
            or ECOMMERCESERVICES
        merchant_customer_identification (Union[Unset, str]): Merchant customer identification, must be specified if
            paymentContextCode is either ECOMMERCEGOODS or ECOMMERCESERVICES
    """

    payment_context_code: PispgatewayLegacyPaymentContextPaymentContextCode
    delivery_address: Union[Unset, "PispgatewayDeliveryAddress"] = UNSET
    merchant_category_code: Union[Unset, str] = UNSET
    merchant_customer_identification: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payment_context_code = self.payment_context_code.value

        delivery_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_address, Unset):
            delivery_address = self.delivery_address.to_dict()

        merchant_category_code = self.merchant_category_code
        merchant_customer_identification = self.merchant_customer_identification

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "paymentContextCode": payment_context_code,
            }
        )
        if delivery_address is not UNSET:
            field_dict["deliveryAddress"] = delivery_address
        if merchant_category_code is not UNSET:
            field_dict["merchantCategoryCode"] = merchant_category_code
        if merchant_customer_identification is not UNSET:
            field_dict["merchantCustomerIdentification"] = merchant_customer_identification

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_delivery_address import PispgatewayDeliveryAddress

        d = src_dict.copy()
        payment_context_code = PispgatewayLegacyPaymentContextPaymentContextCode(
            d.pop("paymentContextCode")
        )

        _delivery_address = d.pop("deliveryAddress", UNSET)
        delivery_address: Union[Unset, PispgatewayDeliveryAddress]
        if isinstance(_delivery_address, Unset):
            delivery_address = UNSET
        else:
            delivery_address = PispgatewayDeliveryAddress.from_dict(_delivery_address)

        merchant_category_code = d.pop("merchantCategoryCode", UNSET)

        merchant_customer_identification = d.pop("merchantCustomerIdentification", UNSET)

        pispgateway_legacy_payment_context = cls(
            payment_context_code=payment_context_code,
            delivery_address=delivery_address,
            merchant_category_code=merchant_category_code,
            merchant_customer_identification=merchant_customer_identification,
        )

        pispgateway_legacy_payment_context.additional_properties = d
        return pispgateway_legacy_payment_context

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
