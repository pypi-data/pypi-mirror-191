from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.card_one_time_token_request_purpose import CardOneTimeTokenRequestPurpose
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardOneTimeTokenRequest")


@attr.s(auto_attribs=True)
class CardOneTimeTokenRequest:
    """
    Attributes:
        public_key (Union[Unset, str]): Base64 UTF-8 encoded RSA public key to be used to encrypt the token in the
            response. The key must be at least 4096 bits in length.
        purpose (Union[Unset, CardOneTimeTokenRequestPurpose]): What the token will be used for. UPDATE tokens cannot be
            used for READ purposes, and READ tokens cannot be used for updates. Default:
            CardOneTimeTokenRequestPurpose.READ.
    """

    public_key: Union[Unset, str] = UNSET
    purpose: Union[Unset, CardOneTimeTokenRequestPurpose] = CardOneTimeTokenRequestPurpose.READ
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        public_key = self.public_key
        purpose: Union[Unset, str] = UNSET
        if not isinstance(self.purpose, Unset):
            purpose = self.purpose.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if public_key is not UNSET:
            field_dict["publicKey"] = public_key
        if purpose is not UNSET:
            field_dict["purpose"] = purpose

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        public_key = d.pop("publicKey", UNSET)

        _purpose = d.pop("purpose", UNSET)
        purpose: Union[Unset, CardOneTimeTokenRequestPurpose]
        if isinstance(_purpose, Unset):
            purpose = UNSET
        else:
            purpose = CardOneTimeTokenRequestPurpose(_purpose)

        card_one_time_token_request = cls(
            public_key=public_key,
            purpose=purpose,
        )

        card_one_time_token_request.additional_properties = d
        return card_one_time_token_request

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
