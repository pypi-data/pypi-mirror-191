import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.directdebit_collection_schedule_response_status import (
    DirectdebitCollectionScheduleResponseStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DirectdebitCollectionScheduleResponse")


@attr.s(auto_attribs=True)
class DirectdebitCollectionScheduleResponse:
    """
    Attributes:
        created_date (datetime.datetime): Datetime when direct-debit collection was created.Format is 'yyyy-MM-
            dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        frequency (str): Frequency for direct-debit collection Example: MONTHLY.
        id (str): Unique id for direct-debit collection. Example: Q0000001.
        number_of_payments (int): Number of payments for direct-debit collection Example: 12.
        status (DirectdebitCollectionScheduleResponseStatus): Status of the direct-debit collection. Can be one of
            ACTIVE, PENDING, SUBMITTED, REJECTED, CANCELLED Example: PROCESSING.
        external_reference (Union[Unset, str]):
        first_payment_amount (Union[Unset, float]): Amount of the first collection payment Example: 100.
        first_payment_date (Union[Unset, str]): Date of the first collection payment. Format is yyyy-MM-dd. Example:
            2018-01-10.
        regular_payment_amount (Union[Unset, float]): Amount of the regular collection payments Example: 100.
        regular_payment_start_date (Union[Unset, str]): Start date of the regular collection payment. Format is yyyy-MM-
            dd. Example: 2018-01-10.
    """

    created_date: datetime.datetime
    frequency: str
    id: str
    number_of_payments: int
    status: DirectdebitCollectionScheduleResponseStatus
    external_reference: Union[Unset, str] = UNSET
    first_payment_amount: Union[Unset, float] = UNSET
    first_payment_date: Union[Unset, str] = UNSET
    regular_payment_amount: Union[Unset, float] = UNSET
    regular_payment_start_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_date = self.created_date.isoformat()

        frequency = self.frequency
        id = self.id
        number_of_payments = self.number_of_payments
        status = self.status.value

        external_reference = self.external_reference
        first_payment_amount = self.first_payment_amount
        first_payment_date = self.first_payment_date
        regular_payment_amount = self.regular_payment_amount
        regular_payment_start_date = self.regular_payment_start_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdDate": created_date,
                "frequency": frequency,
                "id": id,
                "numberOfPayments": number_of_payments,
                "status": status,
            }
        )
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if first_payment_amount is not UNSET:
            field_dict["firstPaymentAmount"] = first_payment_amount
        if first_payment_date is not UNSET:
            field_dict["firstPaymentDate"] = first_payment_date
        if regular_payment_amount is not UNSET:
            field_dict["regularPaymentAmount"] = regular_payment_amount
        if regular_payment_start_date is not UNSET:
            field_dict["regularPaymentStartDate"] = regular_payment_start_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_date = isoparse(d.pop("createdDate"))

        frequency = d.pop("frequency")

        id = d.pop("id")

        number_of_payments = d.pop("numberOfPayments")

        status = DirectdebitCollectionScheduleResponseStatus(d.pop("status"))

        external_reference = d.pop("externalReference", UNSET)

        first_payment_amount = d.pop("firstPaymentAmount", UNSET)

        first_payment_date = d.pop("firstPaymentDate", UNSET)

        regular_payment_amount = d.pop("regularPaymentAmount", UNSET)

        regular_payment_start_date = d.pop("regularPaymentStartDate", UNSET)

        directdebit_collection_schedule_response = cls(
            created_date=created_date,
            frequency=frequency,
            id=id,
            number_of_payments=number_of_payments,
            status=status,
            external_reference=external_reference,
            first_payment_amount=first_payment_amount,
            first_payment_date=first_payment_date,
            regular_payment_amount=regular_payment_amount,
            regular_payment_start_date=regular_payment_start_date,
        )

        directdebit_collection_schedule_response.additional_properties = d
        return directdebit_collection_schedule_response

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
