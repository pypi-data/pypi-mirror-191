from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.card_card_response import CardCardResponse


T = TypeVar("T", bound="CardCardPageResponseCardResponse")


@attr.s(auto_attribs=True)
class CardCardPageResponseCardResponse:
    """
    Attributes:
        content (List['CardCardResponse']): List of responses on the current page
        page (int): Current page number, 0 based; i.e first-page = 0, second-page = 1
        size (int): Page size
        total_pages (int): Total pages
        total_size (int): Total count
    """

    content: List["CardCardResponse"]
    page: int
    size: int
    total_pages: int
    total_size: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = []
        for content_item_data in self.content:
            content_item = content_item_data.to_dict()

            content.append(content_item)

        page = self.page
        size = self.size
        total_pages = self.total_pages
        total_size = self.total_size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "page": page,
                "size": size,
                "totalPages": total_pages,
                "totalSize": total_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_card_response import CardCardResponse

        d = src_dict.copy()
        content = []
        _content = d.pop("content")
        for content_item_data in _content:
            content_item = CardCardResponse.from_dict(content_item_data)

            content.append(content_item)

        page = d.pop("page")

        size = d.pop("size")

        total_pages = d.pop("totalPages")

        total_size = d.pop("totalSize")

        card_card_page_response_card_response = cls(
            content=content,
            page=page,
            size=size,
            total_pages=total_pages,
            total_size=total_size,
        )

        card_card_page_response_card_response.additional_properties = d
        return card_card_page_response_card_response

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
