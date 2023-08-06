import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CardCreateCardResponse")


@attr.s(auto_attribs=True)
class CardCreateCardResponse:
    """
    Attributes:
        created_date (datetime.datetime): The creation date of the card
        cvv2 (str): Card CVV2 number.
        external_ref (str): Client reference for the newly created card.
        id (str): Card identifier. Maximum of 10 alphanumeric characters.
        max_limit (str): Maximum Limit which can be set on this card and is the maximum lifetime spend the card can have
            Example: 4000.0.
        pan (str): Full card PAN.
        masked_pan (Union[Unset, str]): Masked card PAN.
    """

    created_date: datetime.datetime
    cvv2: str
    external_ref: str
    id: str
    max_limit: str
    pan: str
    masked_pan: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_date = self.created_date.isoformat()

        cvv2 = self.cvv2
        external_ref = self.external_ref
        id = self.id
        max_limit = self.max_limit
        pan = self.pan
        masked_pan = self.masked_pan

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdDate": created_date,
                "cvv2": cvv2,
                "externalRef": external_ref,
                "id": id,
                "maxLimit": max_limit,
                "pan": pan,
            }
        )
        if masked_pan is not UNSET:
            field_dict["maskedPan"] = masked_pan

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_date = isoparse(d.pop("createdDate"))

        cvv2 = d.pop("cvv2")

        external_ref = d.pop("externalRef")

        id = d.pop("id")

        max_limit = d.pop("maxLimit")

        pan = d.pop("pan")

        masked_pan = d.pop("maskedPan", UNSET)

        card_create_card_response = cls(
            created_date=created_date,
            cvv2=cvv2,
            external_ref=external_ref,
            id=id,
            max_limit=max_limit,
            pan=pan,
            masked_pan=masked_pan,
        )

        card_create_card_response.additional_properties = d
        return card_create_card_response

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
