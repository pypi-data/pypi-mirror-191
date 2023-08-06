from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentSchemeInfo")


@attr.s(auto_attribs=True)
class PaymentSchemeInfo:
    """Information with regards to the payment scheme

    Attributes:
        id (Union[Unset, str]):
        message (Union[Unset, str]):
        name (Union[Unset, str]):
        response_code (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    response_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        message = self.message
        name = self.name
        response_code = self.response_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if message is not UNSET:
            field_dict["message"] = message
        if name is not UNSET:
            field_dict["name"] = name
        if response_code is not UNSET:
            field_dict["responseCode"] = response_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        message = d.pop("message", UNSET)

        name = d.pop("name", UNSET)

        response_code = d.pop("responseCode", UNSET)

        payment_scheme_info = cls(
            id=id,
            message=message,
            name=name,
            response_code=response_code,
        )

        payment_scheme_info.additional_properties = d
        return payment_scheme_info

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
