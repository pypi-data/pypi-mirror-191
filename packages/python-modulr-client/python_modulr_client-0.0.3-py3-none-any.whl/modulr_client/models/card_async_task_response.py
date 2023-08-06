import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.card_async_task_response_status import CardAsyncTaskResponseStatus
from ..models.card_async_task_response_type import CardAsyncTaskResponseType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardAsyncTaskResponse")


@attr.s(auto_attribs=True)
class CardAsyncTaskResponse:
    """List of responses on the current page

    Attributes:
        created_date (datetime.datetime): The creation date of the task
        status (CardAsyncTaskResponseStatus): Status of the task
        task_bid (str): ID of async task Example: T110000003.
        type (CardAsyncTaskResponseType): Type of async task
        error_reason (Union[Unset, str]): The error reason. Only populated if status is ERROR
        resource_id (Union[Unset, str]): ID of resource after task completion. Will only be returned for COMPLETE tasks.
            Example: V110000022.
        resource_url (Union[Unset, str]): Url of available resource after task completion Example: /cards/V110000022.
    """

    created_date: datetime.datetime
    status: CardAsyncTaskResponseStatus
    task_bid: str
    type: CardAsyncTaskResponseType
    error_reason: Union[Unset, str] = UNSET
    resource_id: Union[Unset, str] = UNSET
    resource_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_date = self.created_date.isoformat()

        status = self.status.value

        task_bid = self.task_bid
        type = self.type.value

        error_reason = self.error_reason
        resource_id = self.resource_id
        resource_url = self.resource_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdDate": created_date,
                "status": status,
                "taskBid": task_bid,
                "type": type,
            }
        )
        if error_reason is not UNSET:
            field_dict["errorReason"] = error_reason
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if resource_url is not UNSET:
            field_dict["resourceUrl"] = resource_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_date = isoparse(d.pop("createdDate"))

        status = CardAsyncTaskResponseStatus(d.pop("status"))

        task_bid = d.pop("taskBid")

        type = CardAsyncTaskResponseType(d.pop("type"))

        error_reason = d.pop("errorReason", UNSET)

        resource_id = d.pop("resourceId", UNSET)

        resource_url = d.pop("resourceUrl", UNSET)

        card_async_task_response = cls(
            created_date=created_date,
            status=status,
            task_bid=task_bid,
            type=type,
            error_reason=error_reason,
            resource_id=resource_id,
            resource_url=resource_url,
        )

        card_async_task_response.additional_properties = d
        return card_async_task_response

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
