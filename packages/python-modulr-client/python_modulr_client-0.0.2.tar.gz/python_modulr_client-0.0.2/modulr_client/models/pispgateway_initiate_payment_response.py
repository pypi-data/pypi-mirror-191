from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayInitiatePaymentResponse")


@attr.s(auto_attribs=True)
class PispgatewayInitiatePaymentResponse:
    """Response object to Initiate Payment

    Attributes:
        payment_initiation_id (Union[Unset, str]): The unique identifier of the payment initiation request at Modulr
            Example: I000000001.
        redirect_url (Union[Unset, str]): A redirect URL for the user to authorise the payment initiation request at the
            ASPSP Example: https://www.bankofmoney.com/authorize.
    """

    payment_initiation_id: Union[Unset, str] = UNSET
    redirect_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payment_initiation_id = self.payment_initiation_id
        redirect_url = self.redirect_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payment_initiation_id is not UNSET:
            field_dict["paymentInitiationId"] = payment_initiation_id
        if redirect_url is not UNSET:
            field_dict["redirectUrl"] = redirect_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payment_initiation_id = d.pop("paymentInitiationId", UNSET)

        redirect_url = d.pop("redirectUrl", UNSET)

        pispgateway_initiate_payment_response = cls(
            payment_initiation_id=payment_initiation_id,
            redirect_url=redirect_url,
        )

        pispgateway_initiate_payment_response.additional_properties = d
        return pispgateway_initiate_payment_response

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
