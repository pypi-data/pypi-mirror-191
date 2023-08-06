from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.notification_notification_request_channel import (
    NotificationNotificationRequestChannel,
)
from ..models.notification_notification_request_type import (
    NotificationNotificationRequestType,
)

if TYPE_CHECKING:
    from ..models.notification_notification_config import NotificationNotificationConfig


T = TypeVar("T", bound="NotificationNotificationRequest")


@attr.s(auto_attribs=True)
class NotificationNotificationRequest:
    """
    Attributes:
        channel (NotificationNotificationRequestChannel): Channel used for sending the notification
        config (NotificationNotificationConfig): Configuration information for this Notification entity.
        destinations (List[str]): The list of emails or url(webhook) used for sending the notification. For 'EMAIL'
            channel this can be a list of comma separated email addresses. For 'WEBHOOK' channel this should be a single
            URL.
        type (NotificationNotificationRequestType): Type of the notification.
    """

    channel: NotificationNotificationRequestChannel
    config: "NotificationNotificationConfig"
    destinations: List[str]
    type: NotificationNotificationRequestType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel = self.channel.value

        config = self.config.to_dict()

        destinations = self.destinations

        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel": channel,
                "config": config,
                "destinations": destinations,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.notification_notification_config import (
            NotificationNotificationConfig,
        )

        d = src_dict.copy()
        channel = NotificationNotificationRequestChannel(d.pop("channel"))

        config = NotificationNotificationConfig.from_dict(d.pop("config"))

        destinations = cast(List[str], d.pop("destinations"))

        type = NotificationNotificationRequestType(d.pop("type"))

        notification_notification_request = cls(
            channel=channel,
            config=config,
            destinations=destinations,
            type=type,
        )

        notification_notification_request.additional_properties = d
        return notification_notification_request

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
