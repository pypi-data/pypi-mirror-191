import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.payment_batch_payment_details_response_status import (
    PaymentBatchPaymentDetailsResponseStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_batch_payment_approval import PaymentBatchPaymentApproval
    from ..models.payment_batch_payment_details_response_payment_details import (
        PaymentBatchPaymentDetailsResponsePaymentDetails,
    )
    from ..models.payment_batch_payment_summary import PaymentBatchPaymentSummary
    from ..models.payment_payment_response import PaymentPaymentResponse


T = TypeVar("T", bound="PaymentBatchPaymentDetailsResponse")


@attr.s(auto_attribs=True)
class PaymentBatchPaymentDetailsResponse:
    """
    Attributes:
        payment_responses (List['PaymentPaymentResponse']): Full details of all payments in this batch
        approvals (Union[Unset, List['PaymentBatchPaymentApproval']]): List of batch-level approvals
        created_date (Union[Unset, datetime.datetime]): Datetime when the batch payment was created. Format is 'yyyy-MM-
            dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        current_user_can_approve (Union[Unset, bool]): Whether the user is allowed to approve this batch, based on their
            approval limits, and applicable configuration Example: True.
        current_user_can_cancel (Union[Unset, bool]): Whether the user is allowed and currently able to cancel at least
            one of the payments in this batch
        external_reference (Union[Unset, str]): External reference, if provided Example: aReference_00001.
        id (Union[Unset, str]): Unique id for the Batch Payment. 10 characters long Example: D920000001.
        payment_details (Union[Unset, PaymentBatchPaymentDetailsResponsePaymentDetails]): Summary of payments and
            approvals, per currency (as a 3-alpha currency code)
        status (Union[Unset, PaymentBatchPaymentDetailsResponseStatus]): Current status of batch. Example: ACCEPTED.
        summary (Union[Unset, PaymentBatchPaymentSummary]): Summary of the state of payment requests in this batch
        total_payments (Union[Unset, int]): Total count of payments in this batch Example: 9123.
    """

    payment_responses: List["PaymentPaymentResponse"]
    approvals: Union[Unset, List["PaymentBatchPaymentApproval"]] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    current_user_can_approve: Union[Unset, bool] = UNSET
    current_user_can_cancel: Union[Unset, bool] = UNSET
    external_reference: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    payment_details: Union[Unset, "PaymentBatchPaymentDetailsResponsePaymentDetails"] = UNSET
    status: Union[Unset, PaymentBatchPaymentDetailsResponseStatus] = UNSET
    summary: Union[Unset, "PaymentBatchPaymentSummary"] = UNSET
    total_payments: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payment_responses = []
        for payment_responses_item_data in self.payment_responses:
            payment_responses_item = payment_responses_item_data.to_dict()

            payment_responses.append(payment_responses_item)

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

        summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        total_payments = self.total_payments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "paymentResponses": payment_responses,
            }
        )
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
        if summary is not UNSET:
            field_dict["summary"] = summary
        if total_payments is not UNSET:
            field_dict["totalPayments"] = total_payments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_batch_payment_approval import PaymentBatchPaymentApproval
        from ..models.payment_batch_payment_details_response_payment_details import (
            PaymentBatchPaymentDetailsResponsePaymentDetails,
        )
        from ..models.payment_batch_payment_summary import PaymentBatchPaymentSummary
        from ..models.payment_payment_response import PaymentPaymentResponse

        d = src_dict.copy()
        payment_responses = []
        _payment_responses = d.pop("paymentResponses")
        for payment_responses_item_data in _payment_responses:
            payment_responses_item = PaymentPaymentResponse.from_dict(payment_responses_item_data)

            payment_responses.append(payment_responses_item)

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
        payment_details: Union[Unset, PaymentBatchPaymentDetailsResponsePaymentDetails]
        if isinstance(_payment_details, Unset):
            payment_details = UNSET
        else:
            payment_details = PaymentBatchPaymentDetailsResponsePaymentDetails.from_dict(
                _payment_details
            )

        _status = d.pop("status", UNSET)
        status: Union[Unset, PaymentBatchPaymentDetailsResponseStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PaymentBatchPaymentDetailsResponseStatus(_status)

        _summary = d.pop("summary", UNSET)
        summary: Union[Unset, PaymentBatchPaymentSummary]
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = PaymentBatchPaymentSummary.from_dict(_summary)

        total_payments = d.pop("totalPayments", UNSET)

        payment_batch_payment_details_response = cls(
            payment_responses=payment_responses,
            approvals=approvals,
            created_date=created_date,
            current_user_can_approve=current_user_can_approve,
            current_user_can_cancel=current_user_can_cancel,
            external_reference=external_reference,
            id=id,
            payment_details=payment_details,
            status=status,
            summary=summary,
            total_payments=total_payments,
        )

        payment_batch_payment_details_response.additional_properties = d
        return payment_batch_payment_details_response

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
