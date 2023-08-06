import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.notification_web_hook_failure_response_event_name import (
    NotificationWebHookFailureResponseEventName,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_web_hook_failure_response_data import (
        NotificationWebHookFailureResponseData,
    )


T = TypeVar("T", bound="NotificationWebHookFailureResponse")


@attr.s(auto_attribs=True)
class NotificationWebHookFailureResponse:
    """
    Attributes:
        customer_bid (str): Unique Identifier for the customer of this webhook.
        event_name (NotificationWebHookFailureResponseEventName): Event which would trigger the webhook
        last_failed_time (datetime.datetime): Last failure time. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC
            offset. e.g '2017-01-28T01:01:01+0000'
        retry (bool): Turn webhook retry mechanism on/off
        url (str): Endpoint URL for receiving webhook data
        data (Union[Unset, NotificationWebHookFailureResponseData]):
    """

    customer_bid: str
    event_name: NotificationWebHookFailureResponseEventName
    last_failed_time: datetime.datetime
    retry: bool
    url: str
    data: Union[Unset, "NotificationWebHookFailureResponseData"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        customer_bid = self.customer_bid
        event_name = self.event_name.value

        last_failed_time = self.last_failed_time.isoformat()

        retry = self.retry
        url = self.url
        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customerBid": customer_bid,
                "eventName": event_name,
                "lastFailedTime": last_failed_time,
                "retry": retry,
                "url": url,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.notification_web_hook_failure_response_data import (
            NotificationWebHookFailureResponseData,
        )

        d = src_dict.copy()
        customer_bid = d.pop("customerBid")

        event_name = NotificationWebHookFailureResponseEventName(d.pop("eventName"))

        last_failed_time = isoparse(d.pop("lastFailedTime"))

        retry = d.pop("retry")

        url = d.pop("url")

        _data = d.pop("data", UNSET)
        data: Union[Unset, NotificationWebHookFailureResponseData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = NotificationWebHookFailureResponseData.from_dict(_data)

        notification_web_hook_failure_response = cls(
            customer_bid=customer_bid,
            event_name=event_name,
            last_failed_time=last_failed_time,
            retry=retry,
            url=url,
            data=data,
        )

        notification_web_hook_failure_response.additional_properties = d
        return notification_web_hook_failure_response

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
