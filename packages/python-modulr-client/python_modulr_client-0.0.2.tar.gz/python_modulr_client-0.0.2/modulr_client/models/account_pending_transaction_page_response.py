from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_pending_transaction_response import (
        AccountPendingTransactionResponse,
    )


T = TypeVar("T", bound="AccountPendingTransactionPageResponse")


@attr.s(auto_attribs=True)
class AccountPendingTransactionPageResponse:
    """
    Attributes:
        content (List['AccountPendingTransactionResponse']): List of responses on the current page
        page (int): Current page number, 0 based; i.e first-page = 0, second-page = 1
        size (int): Page size
        total_pages (int): Total pages
        total_size (int): Total count
        page_start_balance (Union[Unset, float]): The sum of the pending transactions up to this page.
            This is only present if there are no filters other than page and size defined Example: 250.3.
    """

    content: List["AccountPendingTransactionResponse"]
    page: int
    size: int
    total_pages: int
    total_size: int
    page_start_balance: Union[Unset, float] = UNSET
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
        page_start_balance = self.page_start_balance

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
        if page_start_balance is not UNSET:
            field_dict["pageStartBalance"] = page_start_balance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_pending_transaction_response import (
            AccountPendingTransactionResponse,
        )

        d = src_dict.copy()
        content = []
        _content = d.pop("content")
        for content_item_data in _content:
            content_item = AccountPendingTransactionResponse.from_dict(content_item_data)

            content.append(content_item)

        page = d.pop("page")

        size = d.pop("size")

        total_pages = d.pop("totalPages")

        total_size = d.pop("totalSize")

        page_start_balance = d.pop("pageStartBalance", UNSET)

        account_pending_transaction_page_response = cls(
            content=content,
            page=page,
            size=size,
            total_pages=total_pages,
            total_size=total_size,
            page_start_balance=page_start_balance,
        )

        account_pending_transaction_page_response.additional_properties = d
        return account_pending_transaction_page_response

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
