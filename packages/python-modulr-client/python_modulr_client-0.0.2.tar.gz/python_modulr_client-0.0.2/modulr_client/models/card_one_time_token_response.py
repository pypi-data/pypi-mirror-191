from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardOneTimeTokenResponse")


@attr.s(auto_attribs=True)
class CardOneTimeTokenResponse:
    """
    Attributes:
        encrypted (bool): Whether this token is encrypted
        token (str): The token to use by the client for retrieving card details. Where 'encrypted' is true, this will be
            a value that must be decrypted on the client device before being used in subsequent API calls Example:
            eyJ0....zRyk.
        encrypted_symmetric_key (Union[Unset, str]): Base64 UTF-8 encoded Symmetric key used to encrypt token, encrypted
            with client's public key. Only provided if 'encrypted' is true.
        initialisation_vector (Union[Unset, str]): Base64 UTF-8 encoded initialisation vector used with symmetric key
            for encrypting the token. Only provided if 'encrypted' is true.
    """

    encrypted: bool
    token: str
    encrypted_symmetric_key: Union[Unset, str] = UNSET
    initialisation_vector: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        encrypted = self.encrypted
        token = self.token
        encrypted_symmetric_key = self.encrypted_symmetric_key
        initialisation_vector = self.initialisation_vector

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "encrypted": encrypted,
                "token": token,
            }
        )
        if encrypted_symmetric_key is not UNSET:
            field_dict["encryptedSymmetricKey"] = encrypted_symmetric_key
        if initialisation_vector is not UNSET:
            field_dict["initialisationVector"] = initialisation_vector

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        encrypted = d.pop("encrypted")

        token = d.pop("token")

        encrypted_symmetric_key = d.pop("encryptedSymmetricKey", UNSET)

        initialisation_vector = d.pop("initialisationVector", UNSET)

        card_one_time_token_response = cls(
            encrypted=encrypted,
            token=token,
            encrypted_symmetric_key=encrypted_symmetric_key,
            initialisation_vector=initialisation_vector,
        )

        card_one_time_token_response.additional_properties = d
        return card_one_time_token_response

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
