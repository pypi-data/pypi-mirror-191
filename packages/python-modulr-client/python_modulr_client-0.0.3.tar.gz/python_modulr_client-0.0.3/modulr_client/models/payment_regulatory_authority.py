from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.payment_regulatory_authority_authority_country import (
    PaymentRegulatoryAuthorityAuthorityCountry,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentRegulatoryAuthority")


@attr.s(auto_attribs=True)
class PaymentRegulatoryAuthority:
    """Regulatory authority

    Attributes:
        authority_country (Union[Unset, PaymentRegulatoryAuthorityAuthorityCountry]): ISO 3166 country code of the
            ultimate payers address Example: GB.
        authority_name (Union[Unset, str]): Authority name. Maximum of 70 characters. Example: Financial Conduct
            Authority.
    """

    authority_country: Union[Unset, PaymentRegulatoryAuthorityAuthorityCountry] = UNSET
    authority_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        authority_country: Union[Unset, str] = UNSET
        if not isinstance(self.authority_country, Unset):
            authority_country = self.authority_country.value

        authority_name = self.authority_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if authority_country is not UNSET:
            field_dict["authorityCountry"] = authority_country
        if authority_name is not UNSET:
            field_dict["authorityName"] = authority_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _authority_country = d.pop("authorityCountry", UNSET)
        authority_country: Union[Unset, PaymentRegulatoryAuthorityAuthorityCountry]
        if isinstance(_authority_country, Unset):
            authority_country = UNSET
        else:
            authority_country = PaymentRegulatoryAuthorityAuthorityCountry(_authority_country)

        authority_name = d.pop("authorityName", UNSET)

        payment_regulatory_authority = cls(
            authority_country=authority_country,
            authority_name=authority_name,
        )

        payment_regulatory_authority.additional_properties = d
        return payment_regulatory_authority

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
