from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayInitiateStandingOrderResponse")


@attr.s(auto_attribs=True)
class PispgatewayInitiateStandingOrderResponse:
    """Response object to Initiate Standing Order

    Attributes:
        redirect_url (Union[Unset, str]): A redirect URL for the user to authorise the standing order initiation request
            at the ASPSP Example: https://www.bankofmoney.com/authorize.
        standing_order_initiation_id (Union[Unset, str]): The unique identifier of the standing order initiation request
            at Modulr Example: I000000001.
    """

    redirect_url: Union[Unset, str] = UNSET
    standing_order_initiation_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        redirect_url = self.redirect_url
        standing_order_initiation_id = self.standing_order_initiation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if redirect_url is not UNSET:
            field_dict["redirectUrl"] = redirect_url
        if standing_order_initiation_id is not UNSET:
            field_dict["standingOrderInitiationId"] = standing_order_initiation_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        redirect_url = d.pop("redirectUrl", UNSET)

        standing_order_initiation_id = d.pop("standingOrderInitiationId", UNSET)

        pispgateway_initiate_standing_order_response = cls(
            redirect_url=redirect_url,
            standing_order_initiation_id=standing_order_initiation_id,
        )

        pispgateway_initiate_standing_order_response.additional_properties = d
        return pispgateway_initiate_standing_order_response

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
