from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.card_card_replacement_request_reason import (
    CardCardReplacementRequestReason,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_product_design_detail import CardProductDesignDetail


T = TypeVar("T", bound="CardCardReplacementRequest")


@attr.s(auto_attribs=True)
class CardCardReplacementRequest:
    """Replacement

    Attributes:
        reason (CardCardReplacementRequestReason): The reason for replacing the card. Can be one of DAMAGED (physical
            only), LOST, STOLEN, RENEW Example: STOLEN.
        design (Union[Unset, CardProductDesignDetail]): Design references for physical card and packaging
        external_ref (Union[Unset, str]): Client reference for the newly created card. Maximum of 50 alphanumeric
            characters (including underscore, hyphen and space).
    """

    reason: CardCardReplacementRequestReason
    design: Union[Unset, "CardProductDesignDetail"] = UNSET
    external_ref: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        design: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.design, Unset):
            design = self.design.to_dict()

        external_ref = self.external_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
            }
        )
        if design is not UNSET:
            field_dict["design"] = design
        if external_ref is not UNSET:
            field_dict["externalRef"] = external_ref

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_product_design_detail import CardProductDesignDetail

        d = src_dict.copy()
        reason = CardCardReplacementRequestReason(d.pop("reason"))

        _design = d.pop("design", UNSET)
        design: Union[Unset, CardProductDesignDetail]
        if isinstance(_design, Unset):
            design = UNSET
        else:
            design = CardProductDesignDetail.from_dict(_design)

        external_ref = d.pop("externalRef", UNSET)

        card_card_replacement_request = cls(
            reason=reason,
            design=design,
            external_ref=external_ref,
        )

        card_card_replacement_request.additional_properties = d
        return card_card_replacement_request

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
