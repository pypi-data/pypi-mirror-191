import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.payment_batch_payment_status import PaymentBatchPaymentStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_batch_payment_approval import PaymentBatchPaymentApproval
    from ..models.payment_batch_payment_payment_details import (
        PaymentBatchPaymentPaymentDetails,
    )


T = TypeVar("T", bound="PaymentBatchPayment")


@attr.s(auto_attribs=True)
class PaymentBatchPayment:
    """List of responses on the current page

    Attributes:
        approvals (Union[Unset, List['PaymentBatchPaymentApproval']]): List of batch-level approvals
        created_date (Union[Unset, datetime.datetime]): Datetime when the batch payment was created. Format is 'yyyy-MM-
            dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        current_user_can_approve (Union[Unset, bool]): Whether the user is allowed to approve this batch, based on their
            approval limits, and applicable configuration Example: True.
        current_user_can_cancel (Union[Unset, bool]): Whether the user is allowed and currently able to cancel at least
            one of the payments in this batch
        external_reference (Union[Unset, str]): External reference, if provided Example: aReference_00001.
        id (Union[Unset, str]): Unique id for the Batch Payment. 10 characters long Example: D920000001.
        payment_details (Union[Unset, PaymentBatchPaymentPaymentDetails]): Summary of payments and approvals, per
            currency (as a 3-alpha currency code)
        status (Union[Unset, PaymentBatchPaymentStatus]): Current status of batch. Example: ACCEPTED.
        total_payments (Union[Unset, int]): Total count of payments in this batch Example: 9123.
    """

    approvals: Union[Unset, List["PaymentBatchPaymentApproval"]] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    current_user_can_approve: Union[Unset, bool] = UNSET
    current_user_can_cancel: Union[Unset, bool] = UNSET
    external_reference: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    payment_details: Union[Unset, "PaymentBatchPaymentPaymentDetails"] = UNSET
    status: Union[Unset, PaymentBatchPaymentStatus] = UNSET
    total_payments: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approvals: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.approvals, Unset):
            approvals = []
            for approvals_item_data in self.approvals:
                approvals_item = approvals_item_data.to_dict()

                approvals.append(approvals_item)

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        current_user_can_approve = self.current_user_can_approve
        current_user_can_cancel = self.current_user_can_cancel
        external_reference = self.external_reference
        id = self.id
        payment_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payment_details, Unset):
            payment_details = self.payment_details.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        total_payments = self.total_payments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approvals is not UNSET:
            field_dict["approvals"] = approvals
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if current_user_can_approve is not UNSET:
            field_dict["currentUserCanApprove"] = current_user_can_approve
        if current_user_can_cancel is not UNSET:
            field_dict["currentUserCanCancel"] = current_user_can_cancel
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if id is not UNSET:
            field_dict["id"] = id
        if payment_details is not UNSET:
            field_dict["paymentDetails"] = payment_details
        if status is not UNSET:
            field_dict["status"] = status
        if total_payments is not UNSET:
            field_dict["totalPayments"] = total_payments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_batch_payment_approval import PaymentBatchPaymentApproval
        from ..models.payment_batch_payment_payment_details import (
            PaymentBatchPaymentPaymentDetails,
        )

        d = src_dict.copy()
        approvals = []
        _approvals = d.pop("approvals", UNSET)
        for approvals_item_data in _approvals or []:
            approvals_item = PaymentBatchPaymentApproval.from_dict(approvals_item_data)

            approvals.append(approvals_item)

        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date, Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)

        current_user_can_approve = d.pop("currentUserCanApprove", UNSET)

        current_user_can_cancel = d.pop("currentUserCanCancel", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        id = d.pop("id", UNSET)

        _payment_details = d.pop("paymentDetails", UNSET)
        payment_details: Union[Unset, PaymentBatchPaymentPaymentDetails]
        if isinstance(_payment_details, Unset):
            payment_details = UNSET
        else:
            payment_details = PaymentBatchPaymentPaymentDetails.from_dict(_payment_details)

        _status = d.pop("status", UNSET)
        status: Union[Unset, PaymentBatchPaymentStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PaymentBatchPaymentStatus(_status)

        total_payments = d.pop("totalPayments", UNSET)

        payment_batch_payment = cls(
            approvals=approvals,
            created_date=created_date,
            current_user_can_approve=current_user_can_approve,
            current_user_can_cancel=current_user_can_cancel,
            external_reference=external_reference,
            id=id,
            payment_details=payment_details,
            status=status,
            total_payments=total_payments,
        )

        payment_batch_payment.additional_properties = d
        return payment_batch_payment

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
