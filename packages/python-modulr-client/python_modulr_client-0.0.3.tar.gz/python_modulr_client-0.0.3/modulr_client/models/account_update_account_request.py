from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountUpdateAccountRequest")


@attr.s(auto_attribs=True)
class AccountUpdateAccountRequest:
    """Details of account to edit

    Attributes:
        external_reference (Union[Unset, str]): External Reference can only have alphanumeric characters plus
            underscore, hyphen and space up to 50 characters long
        name (Union[Unset, str]): Name for the account, only applicable for 'PCM_INDIVIDUAL' and 'PCM_BUSINESS' customer
            types
    """

    external_reference: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_reference = self.external_reference
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        external_reference = d.pop("externalReference", UNSET)

        name = d.pop("name", UNSET)

        account_update_account_request = cls(
            external_reference=external_reference,
            name=name,
        )

        account_update_account_request.additional_properties = d
        return account_update_account_request

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
