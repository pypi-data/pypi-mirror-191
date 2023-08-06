from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.card_card_knowledge_based_authentication import (
        CardCardKnowledgeBasedAuthentication,
    )


T = TypeVar("T", bound="CardCardAuthentication")


@attr.s(auto_attribs=True)
class CardCardAuthentication:
    """Authentication

    Attributes:
        knowledge_base (List['CardCardKnowledgeBasedAuthentication']): 3DS knowledge-based authentication (KBA) answers
    """

    knowledge_base: List["CardCardKnowledgeBasedAuthentication"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        knowledge_base = []
        for knowledge_base_item_data in self.knowledge_base:
            knowledge_base_item = knowledge_base_item_data.to_dict()

            knowledge_base.append(knowledge_base_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "knowledgeBase": knowledge_base,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_card_knowledge_based_authentication import (
            CardCardKnowledgeBasedAuthentication,
        )

        d = src_dict.copy()
        knowledge_base = []
        _knowledge_base = d.pop("knowledgeBase")
        for knowledge_base_item_data in _knowledge_base:
            knowledge_base_item = CardCardKnowledgeBasedAuthentication.from_dict(
                knowledge_base_item_data
            )

            knowledge_base.append(knowledge_base_item)

        card_card_authentication = cls(
            knowledge_base=knowledge_base,
        )

        card_card_authentication.additional_properties = d
        return card_card_authentication

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
