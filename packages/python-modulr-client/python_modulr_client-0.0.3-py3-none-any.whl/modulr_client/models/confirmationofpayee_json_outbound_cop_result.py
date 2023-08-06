from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.confirmationofpayee_json_outbound_cop_result_code import (
    ConfirmationofpayeeJsonOutboundCopResultCode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfirmationofpayeeJsonOutboundCopResult")


@attr.s(auto_attribs=True)
class ConfirmationofpayeeJsonOutboundCopResult:
    """Account Name Check Result

    Attributes:
        code (ConfirmationofpayeeJsonOutboundCopResultCode): The result of the account name check. Example: MATCHED.
        name (Union[Unset, str]): The actual name on the account (as provided by the participating organisation).
            Example: Joseph Bloggs.
    """

    code: ConfirmationofpayeeJsonOutboundCopResultCode
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code.value

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = ConfirmationofpayeeJsonOutboundCopResultCode(d.pop("code"))

        name = d.pop("name", UNSET)

        confirmationofpayee_json_outbound_cop_result = cls(
            code=code,
            name=name,
        )

        confirmationofpayee_json_outbound_cop_result.additional_properties = d
        return confirmationofpayee_json_outbound_cop_result

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
