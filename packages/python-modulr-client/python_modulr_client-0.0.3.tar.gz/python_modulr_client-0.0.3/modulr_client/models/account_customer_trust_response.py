from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_customer_trust_response_trust_nature import (
    AccountCustomerTrustResponseTrustNature,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountCustomerTrustResponse")


@attr.s(auto_attribs=True)
class AccountCustomerTrustResponse:
    """Trust nature for customers of type trust. Mandatory for type Trust, not to be set for non-trust customers.

    Attributes:
        trust_nature (Union[Unset, AccountCustomerTrustResponseTrustNature]):
    """

    trust_nature: Union[Unset, AccountCustomerTrustResponseTrustNature] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trust_nature: Union[Unset, str] = UNSET
        if not isinstance(self.trust_nature, Unset):
            trust_nature = self.trust_nature.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trust_nature is not UNSET:
            field_dict["trustNature"] = trust_nature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _trust_nature = d.pop("trustNature", UNSET)
        trust_nature: Union[Unset, AccountCustomerTrustResponseTrustNature]
        if isinstance(_trust_nature, Unset):
            trust_nature = UNSET
        else:
            trust_nature = AccountCustomerTrustResponseTrustNature(_trust_nature)

        account_customer_trust_response = cls(
            trust_nature=trust_nature,
        )

        account_customer_trust_response.additional_properties = d
        return account_customer_trust_response

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
