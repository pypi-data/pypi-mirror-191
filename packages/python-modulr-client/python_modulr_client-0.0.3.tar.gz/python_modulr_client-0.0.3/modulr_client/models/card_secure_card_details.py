from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardSecureCardDetails")


@attr.s(auto_attribs=True)
class CardSecureCardDetails:
    """
    Attributes:
        cvv2 (str): CVV Example: 123.
        pan (str): PAN Example: 4567123412341234.
        pin (Union[Unset, str]): PIN Example: 1234.
    """

    cvv2: str
    pan: str
    pin: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cvv2 = self.cvv2
        pan = self.pan
        pin = self.pin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cvv2": cvv2,
                "pan": pan,
            }
        )
        if pin is not UNSET:
            field_dict["pin"] = pin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cvv2 = d.pop("cvv2")

        pan = d.pop("pan")

        pin = d.pop("pin", UNSET)

        card_secure_card_details = cls(
            cvv2=cvv2,
            pan=pan,
            pin=pin,
        )

        card_secure_card_details.additional_properties = d
        return card_secure_card_details

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
