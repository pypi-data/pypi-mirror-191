from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="CardResetCardPinRequest")


@attr.s(auto_attribs=True)
class CardResetCardPinRequest:
    """Reset PIN

    Attributes:
        current_pin (str): Card's current PIN required to reset
        new_pin (str): Card's new PIN to update
    """

    current_pin: str
    new_pin: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        current_pin = self.current_pin
        new_pin = self.new_pin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currentPin": current_pin,
                "newPin": new_pin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        current_pin = d.pop("currentPin")

        new_pin = d.pop("newPin")

        card_reset_card_pin_request = cls(
            current_pin=current_pin,
            new_pin=new_pin,
        )

        card_reset_card_pin_request.additional_properties = d
        return card_reset_card_pin_request

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
