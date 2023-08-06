from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.notification_notification_config_days_to_run_item import (
    NotificationNotificationConfigDaysToRunItem,
)
from ..models.notification_notification_config_hmac_algorithm import (
    NotificationNotificationConfigHmacAlgorithm,
)
from ..models.notification_notification_config_times_to_run_item import (
    NotificationNotificationConfigTimesToRunItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationNotificationConfig")


@attr.s(auto_attribs=True)
class NotificationNotificationConfig:
    """Configuration information for this Notification entity.

    Attributes:
        days_to_run (Union[Unset, List[NotificationNotificationConfigDaysToRunItem]]): Days of the week when to trigger
            the notification. This attribute applies only to 'EMAIL' notifications channel, of type 'BALANCE'.
        hmac_algorithm (Union[Unset, NotificationNotificationConfigHmacAlgorithm]): Signing algorithm that is used in
            Webhook HMAC calculation. This attribute only applies to 'WEBHOOK' notifications channel.
        retry (Union[Unset, bool]): Flag indicating whether failed webhooks should be retried. This attribute applies
            only to 'WEBHOOK' notifications channel.
        secret (Union[Unset, str]): Mandatory for webhook. Secret that is used in HMAC calculation, for webhooks. This
            attribute applies only to 'WEBHOOK' notifications channel.
        threshold (Union[Unset, float]): Amount threshold which triggers the notification. This attribute only applies
            to 'EMAIL' notifications channel, of type 'PAYIN', 'PAYOUT'.
        times_to_run (Union[Unset, List[NotificationNotificationConfigTimesToRunItem]]): Times of the day when to
            trigger the notification. This attribute applies only to 'EMAIL' notifications channel, of type 'BALANCE'.
    """

    days_to_run: Union[Unset, List[NotificationNotificationConfigDaysToRunItem]] = UNSET
    hmac_algorithm: Union[Unset, NotificationNotificationConfigHmacAlgorithm] = UNSET
    retry: Union[Unset, bool] = UNSET
    secret: Union[Unset, str] = UNSET
    threshold: Union[Unset, float] = UNSET
    times_to_run: Union[Unset, List[NotificationNotificationConfigTimesToRunItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        days_to_run: Union[Unset, List[str]] = UNSET
        if not isinstance(self.days_to_run, Unset):
            days_to_run = []
            for days_to_run_item_data in self.days_to_run:
                days_to_run_item = days_to_run_item_data.value

                days_to_run.append(days_to_run_item)

        hmac_algorithm: Union[Unset, str] = UNSET
        if not isinstance(self.hmac_algorithm, Unset):
            hmac_algorithm = self.hmac_algorithm.value

        retry = self.retry
        secret = self.secret
        threshold = self.threshold
        times_to_run: Union[Unset, List[str]] = UNSET
        if not isinstance(self.times_to_run, Unset):
            times_to_run = []
            for times_to_run_item_data in self.times_to_run:
                times_to_run_item = times_to_run_item_data.value

                times_to_run.append(times_to_run_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if days_to_run is not UNSET:
            field_dict["daysToRun"] = days_to_run
        if hmac_algorithm is not UNSET:
            field_dict["hmacAlgorithm"] = hmac_algorithm
        if retry is not UNSET:
            field_dict["retry"] = retry
        if secret is not UNSET:
            field_dict["secret"] = secret
        if threshold is not UNSET:
            field_dict["threshold"] = threshold
        if times_to_run is not UNSET:
            field_dict["timesToRun"] = times_to_run

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        days_to_run = []
        _days_to_run = d.pop("daysToRun", UNSET)
        for days_to_run_item_data in _days_to_run or []:
            days_to_run_item = NotificationNotificationConfigDaysToRunItem(days_to_run_item_data)

            days_to_run.append(days_to_run_item)

        _hmac_algorithm = d.pop("hmacAlgorithm", UNSET)
        hmac_algorithm: Union[Unset, NotificationNotificationConfigHmacAlgorithm]
        if isinstance(_hmac_algorithm, Unset):
            hmac_algorithm = UNSET
        else:
            hmac_algorithm = NotificationNotificationConfigHmacAlgorithm(_hmac_algorithm)

        retry = d.pop("retry", UNSET)

        secret = d.pop("secret", UNSET)

        threshold = d.pop("threshold", UNSET)

        times_to_run = []
        _times_to_run = d.pop("timesToRun", UNSET)
        for times_to_run_item_data in _times_to_run or []:
            times_to_run_item = NotificationNotificationConfigTimesToRunItem(
                times_to_run_item_data
            )

            times_to_run.append(times_to_run_item)

        notification_notification_config = cls(
            days_to_run=days_to_run,
            hmac_algorithm=hmac_algorithm,
            retry=retry,
            secret=secret,
            threshold=threshold,
            times_to_run=times_to_run,
        )

        notification_notification_config.additional_properties = d
        return notification_notification_config

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
