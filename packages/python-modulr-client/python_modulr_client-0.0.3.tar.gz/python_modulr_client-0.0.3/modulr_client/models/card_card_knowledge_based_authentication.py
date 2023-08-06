from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.card_card_knowledge_based_authentication_type import (
    CardCardKnowledgeBasedAuthenticationType,
)

T = TypeVar("T", bound="CardCardKnowledgeBasedAuthentication")


@attr.s(auto_attribs=True)
class CardCardKnowledgeBasedAuthentication:
    """3DS Knowledge-Based Authentication (KBA) answers

    Attributes:
        answer (str): 3DS knowledge-based authentication answer
        type (CardCardKnowledgeBasedAuthenticationType): 3DS knowledge-based authentication answer type
    """

    answer: str
    type: CardCardKnowledgeBasedAuthenticationType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answer = self.answer
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer": answer,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        answer = d.pop("answer")

        type = CardCardKnowledgeBasedAuthenticationType(d.pop("type"))

        card_card_knowledge_based_authentication = cls(
            answer=answer,
            type=type,
        )

        card_card_knowledge_based_authentication.additional_properties = d
        return card_card_knowledge_based_authentication

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
