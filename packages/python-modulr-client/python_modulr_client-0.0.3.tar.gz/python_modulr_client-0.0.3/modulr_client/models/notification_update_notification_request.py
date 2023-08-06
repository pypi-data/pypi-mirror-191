from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.notification_update_notification_request_status import (
    NotificationUpdateNotificationRequestStatus,
)

if TYPE_CHECKING:
    from ..models.notification_notification_config import NotificationNotificationConfig


T = TypeVar("T", bound="NotificationUpdateNotificationRequest")


@attr.s(auto_attribs=True)
class NotificationUpdateNotificationRequest:
    """
    Attributes:
        config (NotificationNotificationConfig): Configuration information for this Notification entity.
        destinations (List[str]): The list of emails or url(webhook) used for sending the notification. For 'EMAIL'
            channel this can be a list of comma separated email addresses. For 'WEBHOOK' channel this should be a single
            URL.
        status (NotificationUpdateNotificationRequestStatus): Status of the notification.
    """

    config: "NotificationNotificationConfig"
    destinations: List[str]
    status: NotificationUpdateNotificationRequestStatus
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config = self.config.to_dict()

        destinations = self.destinations

        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "destinations": destinations,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.notification_notification_config import (
            NotificationNotificationConfig,
        )

        d = src_dict.copy()
        config = NotificationNotificationConfig.from_dict(d.pop("config"))

        destinations = cast(List[str], d.pop("destinations"))

        status = NotificationUpdateNotificationRequestStatus(d.pop("status"))

        notification_update_notification_request = cls(
            config=config,
            destinations=destinations,
            status=status,
        )

        notification_update_notification_request.additional_properties = d
        return notification_update_notification_request

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
