from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.card_cancel_card_request_reason import CardCancelCardRequestReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardCancelCardRequest")


@attr.s(auto_attribs=True)
class CardCancelCardRequest:
    """Reason for cancellation

    Attributes:
        reason (Union[Unset, CardCancelCardRequestReason]): The reason for cancelling the card. Can be one of DESTROYED,
            LOST, STOLEN
    """

    reason: Union[Unset, CardCancelCardRequestReason] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, CardCancelCardRequestReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = CardCancelCardRequestReason(_reason)

        card_cancel_card_request = cls(
            reason=reason,
        )

        card_cancel_card_request.additional_properties = d
        return card_cancel_card_request

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
