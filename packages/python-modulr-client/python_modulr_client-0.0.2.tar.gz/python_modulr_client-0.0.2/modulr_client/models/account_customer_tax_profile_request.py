from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AccountCustomerTaxProfileRequest")


@attr.s(auto_attribs=True)
class AccountCustomerTaxProfileRequest:
    """Tax profile for customers of type SOLETRADER. Optional for type SOLETRADER, not to be set for non-SOLETRADER
    customers.

        Attributes:
            tax_identifier (str): Tax identifier for customers of type SOLETRADER. Optional for type SOLETRADER, not to be
                set for non-SOLETRADER customers.
    """

    tax_identifier: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tax_identifier = self.tax_identifier

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "taxIdentifier": tax_identifier,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tax_identifier = d.pop("taxIdentifier")

        account_customer_tax_profile_request = cls(
            tax_identifier=tax_identifier,
        )

        account_customer_tax_profile_request.additional_properties = d
        return account_customer_tax_profile_request

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
