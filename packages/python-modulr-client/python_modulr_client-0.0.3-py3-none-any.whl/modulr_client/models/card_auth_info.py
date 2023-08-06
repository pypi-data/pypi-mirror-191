from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="CardAuthInfo")


@attr.s(auto_attribs=True)
class CardAuthInfo:
    """Authorisation information of the activity

    Attributes:
        input_method (str): Input method
        type (str): Transaction type
    """

    input_method: str
    type: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_method = self.input_method
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputMethod": input_method,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_method = d.pop("inputMethod")

        type = d.pop("type")

        card_auth_info = cls(
            input_method=input_method,
            type=type,
        )

        card_auth_info.additional_properties = d
        return card_auth_info

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
