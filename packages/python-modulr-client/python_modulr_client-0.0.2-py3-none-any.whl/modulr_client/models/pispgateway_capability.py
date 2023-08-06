from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pispgateway_capability_status import PispgatewayCapabilityStatus
from ..models.pispgateway_capability_type import PispgatewayCapabilityType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayCapability")


@attr.s(auto_attribs=True)
class PispgatewayCapability:
    """Capability list of the ASPSP

    Attributes:
        status (Union[Unset, PispgatewayCapabilityStatus]): Status of the capability, can be one of ENABLED, DISABLED
            Example: ENABLED.
        type (Union[Unset, PispgatewayCapabilityType]): Type of the capability, can be one of SINGLE_IMMEDIATE,
            STANDING_ORDER Example: SINGLE_IMMEDIATE.
    """

    status: Union[Unset, PispgatewayCapabilityStatus] = UNSET
    type: Union[Unset, PispgatewayCapabilityType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, PispgatewayCapabilityStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PispgatewayCapabilityStatus(_status)

        _type = d.pop("type", UNSET)
        type: Union[Unset, PispgatewayCapabilityType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PispgatewayCapabilityType(_type)

        pispgateway_capability = cls(
            status=status,
            type=type,
        )

        pispgateway_capability.additional_properties = d
        return pispgateway_capability

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
