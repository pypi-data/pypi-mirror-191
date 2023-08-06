from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_async_task_created_response_meta_data import (
        CardAsyncTaskCreatedResponseMetaData,
    )


T = TypeVar("T", bound="CardAsyncTaskCreatedResponse")


@attr.s(auto_attribs=True)
class CardAsyncTaskCreatedResponse:
    """
    Attributes:
        task_id (str): ID of card task
        task_url (str): Url of card task resource
        meta_data (Union[Unset, CardAsyncTaskCreatedResponseMetaData]): Meta data associated with async task response
    """

    task_id: str
    task_url: str
    meta_data: Union[Unset, "CardAsyncTaskCreatedResponseMetaData"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id
        task_url = self.task_url
        meta_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta_data, Unset):
            meta_data = self.meta_data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "taskId": task_id,
                "taskUrl": task_url,
            }
        )
        if meta_data is not UNSET:
            field_dict["metaData"] = meta_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_async_task_created_response_meta_data import (
            CardAsyncTaskCreatedResponseMetaData,
        )

        d = src_dict.copy()
        task_id = d.pop("taskId")

        task_url = d.pop("taskUrl")

        _meta_data = d.pop("metaData", UNSET)
        meta_data: Union[Unset, CardAsyncTaskCreatedResponseMetaData]
        if isinstance(_meta_data, Unset):
            meta_data = UNSET
        else:
            meta_data = CardAsyncTaskCreatedResponseMetaData.from_dict(_meta_data)

        card_async_task_created_response = cls(
            task_id=task_id,
            task_url=task_url,
            meta_data=meta_data,
        )

        card_async_task_created_response.additional_properties = d
        return card_async_task_created_response

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
