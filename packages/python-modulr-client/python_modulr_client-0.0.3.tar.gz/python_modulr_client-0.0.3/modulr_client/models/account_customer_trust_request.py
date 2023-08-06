from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.account_customer_trust_request_trust_nature import (
    AccountCustomerTrustRequestTrustNature,
)

T = TypeVar("T", bound="AccountCustomerTrustRequest")


@attr.s(auto_attribs=True)
class AccountCustomerTrustRequest:
    """Trust nature for customers of type Trust. Mandatory for type Trust, not to be set for non-trust customers.

    Attributes:
        trust_nature (AccountCustomerTrustRequestTrustNature): Trust nature for customers of type Trust. Mandatory for
            type Trust, not to be set for non-trust customers.
    """

    trust_nature: AccountCustomerTrustRequestTrustNature
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trust_nature = self.trust_nature.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trustNature": trust_nature,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trust_nature = AccountCustomerTrustRequestTrustNature(d.pop("trustNature"))

        account_customer_trust_request = cls(
            trust_nature=trust_nature,
        )

        account_customer_trust_request.additional_properties = d
        return account_customer_trust_request

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
