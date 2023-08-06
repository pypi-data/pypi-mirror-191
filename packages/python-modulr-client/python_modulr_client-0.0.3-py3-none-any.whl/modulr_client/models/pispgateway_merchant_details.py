from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayMerchantDetails")


@attr.s(auto_attribs=True)
class PispgatewayMerchantDetails:
    """Merchant details for the payment context

    Attributes:
        category_code (Union[Unset, str]): Merchant category code conform to ISO 18245, related to the type of services
            or goods provided for the transaction. Must be specified if paymentContextCode is either ECOMMERCEGOODS or
            ECOMMERCESERVICES
        customer_id (Union[Unset, str]): Merchant customer identification, must be specified if paymentContextCode is
            either ECOMMERCEGOODS or ECOMMERCESERVICES
    """

    category_code: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        category_code = self.category_code
        customer_id = self.customer_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if category_code is not UNSET:
            field_dict["categoryCode"] = category_code
        if customer_id is not UNSET:
            field_dict["customerId"] = customer_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        category_code = d.pop("categoryCode", UNSET)

        customer_id = d.pop("customerId", UNSET)

        pispgateway_merchant_details = cls(
            category_code=category_code,
            customer_id=customer_id,
        )

        pispgateway_merchant_details.additional_properties = d
        return pispgateway_merchant_details

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
