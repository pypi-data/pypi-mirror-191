from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="CardProductDesignDetail")


@attr.s(auto_attribs=True)
class CardProductDesignDetail:
    """Design references for physical card and packaging

    Attributes:
        card_ref (str): Design reference for card
        packaging_ref (str): Design reference for card packaging
    """

    card_ref: str
    packaging_ref: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        card_ref = self.card_ref
        packaging_ref = self.packaging_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cardRef": card_ref,
                "packagingRef": packaging_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        card_ref = d.pop("cardRef")

        packaging_ref = d.pop("packagingRef")

        card_product_design_detail = cls(
            card_ref=card_ref,
            packaging_ref=packaging_ref,
        )

        card_product_design_detail.additional_properties = d
        return card_product_design_detail

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
