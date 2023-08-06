from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.payment_regulatory_reporting_type import PaymentRegulatoryReportingType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_regulatory_authority import PaymentRegulatoryAuthority
    from ..models.payment_structured_regulatory_reporting import (
        PaymentStructuredRegulatoryReporting,
    )


T = TypeVar("T", bound="PaymentRegulatoryReporting")


@attr.s(auto_attribs=True)
class PaymentRegulatoryReporting:
    """Regulatory reporting

    Attributes:
        regulatory_authority (Union[Unset, PaymentRegulatoryAuthority]): Regulatory authority
        structured_regulatory_reporting (Union[Unset, PaymentStructuredRegulatoryReporting]): Structured regulatory
            reporting
        type (Union[Unset, PaymentRegulatoryReportingType]): Regulatory Reporting Type Example: CRED.
    """

    regulatory_authority: Union[Unset, "PaymentRegulatoryAuthority"] = UNSET
    structured_regulatory_reporting: Union[Unset, "PaymentStructuredRegulatoryReporting"] = UNSET
    type: Union[Unset, PaymentRegulatoryReportingType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        regulatory_authority: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.regulatory_authority, Unset):
            regulatory_authority = self.regulatory_authority.to_dict()

        structured_regulatory_reporting: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.structured_regulatory_reporting, Unset):
            structured_regulatory_reporting = self.structured_regulatory_reporting.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if regulatory_authority is not UNSET:
            field_dict["regulatoryAuthority"] = regulatory_authority
        if structured_regulatory_reporting is not UNSET:
            field_dict["structuredRegulatoryReporting"] = structured_regulatory_reporting
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_regulatory_authority import PaymentRegulatoryAuthority
        from ..models.payment_structured_regulatory_reporting import (
            PaymentStructuredRegulatoryReporting,
        )

        d = src_dict.copy()
        _regulatory_authority = d.pop("regulatoryAuthority", UNSET)
        regulatory_authority: Union[Unset, PaymentRegulatoryAuthority]
        if isinstance(_regulatory_authority, Unset):
            regulatory_authority = UNSET
        else:
            regulatory_authority = PaymentRegulatoryAuthority.from_dict(_regulatory_authority)

        _structured_regulatory_reporting = d.pop("structuredRegulatoryReporting", UNSET)
        structured_regulatory_reporting: Union[Unset, PaymentStructuredRegulatoryReporting]
        if isinstance(_structured_regulatory_reporting, Unset):
            structured_regulatory_reporting = UNSET
        else:
            structured_regulatory_reporting = PaymentStructuredRegulatoryReporting.from_dict(
                _structured_regulatory_reporting
            )

        _type = d.pop("type", UNSET)
        type: Union[Unset, PaymentRegulatoryReportingType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PaymentRegulatoryReportingType(_type)

        payment_regulatory_reporting = cls(
            regulatory_authority=regulatory_authority,
            structured_regulatory_reporting=structured_regulatory_reporting,
            type=type,
        )

        payment_regulatory_reporting.additional_properties = d
        return payment_regulatory_reporting

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
