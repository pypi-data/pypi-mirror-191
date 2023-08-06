from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.account_additional_personal_identifier_response_type import (
    AccountAdditionalPersonalIdentifierResponseType,
)

T = TypeVar("T", bound="AccountAdditionalPersonalIdentifierResponse")


@attr.s(auto_attribs=True)
class AccountAdditionalPersonalIdentifierResponse:
    """AdditionalPersonalIdentifier

    Attributes:
        type (AccountAdditionalPersonalIdentifierResponseType): The type of Additional Personal Identifier
        value (str): Additional Personal Identifier value
    """

    type: AccountAdditionalPersonalIdentifierResponseType
    value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = AccountAdditionalPersonalIdentifierResponseType(d.pop("type"))

        value = d.pop("value")

        account_additional_personal_identifier_response = cls(
            type=type,
            value=value,
        )

        account_additional_personal_identifier_response.additional_properties = d
        return account_additional_personal_identifier_response

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
