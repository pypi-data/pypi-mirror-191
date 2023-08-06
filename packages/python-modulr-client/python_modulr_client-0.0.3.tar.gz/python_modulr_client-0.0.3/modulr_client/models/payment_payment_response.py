import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.payment_payment_response_approval_status import (
    PaymentPaymentResponseApprovalStatus,
)
from ..models.payment_payment_response_status import PaymentPaymentResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_payment_response_details import PaymentPaymentResponseDetails
    from ..models.payment_scheme_info import PaymentSchemeInfo


T = TypeVar("T", bound="PaymentPaymentResponse")


@attr.s(auto_attribs=True)
class PaymentPaymentResponse:
    """Full details of all payments in this batch

    Attributes:
        details (PaymentPaymentResponseDetails): All the details of the payment from the original request
        external_reference (str): external reference if provided Example: aReference_00001.
        id (str): Unique id for the Payment request. 10 characters long Example: P000001ABC.
        status (PaymentPaymentResponseStatus): Current status of payment. Can be one of [SUBMITTED, SCREENING_REQ,
            VALIDATED, PENDING_FOR_DATE, PENDING_FOR_FUNDS, EXT_PROC, PROCESSED, RECONCILED, ER_INVALID, ER_EXTCONN,
            ER_EXTSYS, ER_EXPIRED, ER_GENERAL, ER_BATCH, EXT_SENT, UNALLOCATED, HELD, RETURNED, CANCELLED, REPROCESSING,
            VOID, CLEARING] Example: VALIDATED.
        approval_status (Union[Unset, PaymentPaymentResponseApprovalStatus]): Current approval status of payment. Can be
            one of [NOTNEEDED, PENDING, APPROVED, REJECTED, DELETED] Example: NOTNEEDED.
        created_date (Union[Unset, datetime.datetime]): Datetime the request was created. Format is 'yyyy-MM-
            dd'T'HH:mm:ss.sssZ' where Z is UTC offset. e.g '2017-01-28T01:01:01.010+0000'
        message (Union[Unset, str]): Information about payment (if available)
        scheme_info (Union[Unset, PaymentSchemeInfo]): Information with regards to the payment scheme
    """

    details: "PaymentPaymentResponseDetails"
    external_reference: str
    id: str
    status: PaymentPaymentResponseStatus
    approval_status: Union[Unset, PaymentPaymentResponseApprovalStatus] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    message: Union[Unset, str] = UNSET
    scheme_info: Union[Unset, "PaymentSchemeInfo"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        details = self.details.to_dict()

        external_reference = self.external_reference
        id = self.id
        status = self.status.value

        approval_status: Union[Unset, str] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        message = self.message
        scheme_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scheme_info, Unset):
            scheme_info = self.scheme_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "details": details,
                "externalReference": external_reference,
                "id": id,
                "status": status,
            }
        )
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if message is not UNSET:
            field_dict["message"] = message
        if scheme_info is not UNSET:
            field_dict["schemeInfo"] = scheme_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_payment_response_details import (
            PaymentPaymentResponseDetails,
        )
        from ..models.payment_scheme_info import PaymentSchemeInfo

        d = src_dict.copy()
        details = PaymentPaymentResponseDetails.from_dict(d.pop("details"))

        external_reference = d.pop("externalReference")

        id = d.pop("id")

        status = PaymentPaymentResponseStatus(d.pop("status"))

        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, PaymentPaymentResponseApprovalStatus]
        if isinstance(_approval_status, Unset):
            approval_status = UNSET
        else:
            approval_status = PaymentPaymentResponseApprovalStatus(_approval_status)

        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date, Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)

        message = d.pop("message", UNSET)

        _scheme_info = d.pop("schemeInfo", UNSET)
        scheme_info: Union[Unset, PaymentSchemeInfo]
        if isinstance(_scheme_info, Unset):
            scheme_info = UNSET
        else:
            scheme_info = PaymentSchemeInfo.from_dict(_scheme_info)

        payment_payment_response = cls(
            details=details,
            external_reference=external_reference,
            id=id,
            status=status,
            approval_status=approval_status,
            created_date=created_date,
            message=message,
            scheme_info=scheme_info,
        )

        payment_payment_response.additional_properties = d
        return payment_payment_response

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
