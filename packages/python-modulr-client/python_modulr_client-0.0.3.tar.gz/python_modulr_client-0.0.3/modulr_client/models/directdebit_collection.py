from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.directdebit_collection_status import DirectdebitCollectionStatus
from ..models.directdebit_collection_type import DirectdebitCollectionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DirectdebitCollection")


@attr.s(auto_attribs=True)
class DirectdebitCollection:
    """List of responses on the current page

    Attributes:
        activity_date (str): collection or reportRaised date for indemnity??? Example: 2018-01-09.
        amount (float): Amount of the collection payment Example: 100.
        id (str): Unique id for a direct-debit collection Example: K000100100.
        mandate_id (str): Unique id for direct-debit mandate. Example: G0000001.
        message (str): Failure description of the payment activity Example: Instruction Cancelled.
        original_activity_date (str): The original scheduled date for a payment to be collected Example: 2018-01-09.
        payer_name (str): Name of the payer Example: Mr John Doe.
        reconciliation_date (str): The reconciled date for a payment to be collected Example: 2018-01-09.
        reconciliation_reference (str): The reconciled reference that links to a payment Example: 2018-01-09.
        status (DirectdebitCollectionStatus): Status of the collection.  Can be one of SUCCESS, FAILED, PROCESSING,
            SCHEDULED, REPRESENTABLE, REPRESENTED, CANCELLED Example: FAILED.
        type (DirectdebitCollectionType): Type of the collection activity.  Can be one of COLLECTION, INDEMNITY Example:
            COLLECTION.
        collection_schedule_id (Union[Unset, str]): Unique id for direct-debit collection schedule for which triggered
            the collection Example: Q9200001.
    """

    activity_date: str
    amount: float
    id: str
    mandate_id: str
    message: str
    original_activity_date: str
    payer_name: str
    reconciliation_date: str
    reconciliation_reference: str
    status: DirectdebitCollectionStatus
    type: DirectdebitCollectionType
    collection_schedule_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        activity_date = self.activity_date
        amount = self.amount
        id = self.id
        mandate_id = self.mandate_id
        message = self.message
        original_activity_date = self.original_activity_date
        payer_name = self.payer_name
        reconciliation_date = self.reconciliation_date
        reconciliation_reference = self.reconciliation_reference
        status = self.status.value

        type = self.type.value

        collection_schedule_id = self.collection_schedule_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activityDate": activity_date,
                "amount": amount,
                "id": id,
                "mandateId": mandate_id,
                "message": message,
                "originalActivityDate": original_activity_date,
                "payerName": payer_name,
                "reconciliationDate": reconciliation_date,
                "reconciliationReference": reconciliation_reference,
                "status": status,
                "type": type,
            }
        )
        if collection_schedule_id is not UNSET:
            field_dict["collectionScheduleId"] = collection_schedule_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activity_date = d.pop("activityDate")

        amount = d.pop("amount")

        id = d.pop("id")

        mandate_id = d.pop("mandateId")

        message = d.pop("message")

        original_activity_date = d.pop("originalActivityDate")

        payer_name = d.pop("payerName")

        reconciliation_date = d.pop("reconciliationDate")

        reconciliation_reference = d.pop("reconciliationReference")

        status = DirectdebitCollectionStatus(d.pop("status"))

        type = DirectdebitCollectionType(d.pop("type"))

        collection_schedule_id = d.pop("collectionScheduleId", UNSET)

        directdebit_collection = cls(
            activity_date=activity_date,
            amount=amount,
            id=id,
            mandate_id=mandate_id,
            message=message,
            original_activity_date=original_activity_date,
            payer_name=payer_name,
            reconciliation_date=reconciliation_date,
            reconciliation_reference=reconciliation_reference,
            status=status,
            type=type,
            collection_schedule_id=collection_schedule_id,
        )

        directdebit_collection.additional_properties = d
        return directdebit_collection

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
