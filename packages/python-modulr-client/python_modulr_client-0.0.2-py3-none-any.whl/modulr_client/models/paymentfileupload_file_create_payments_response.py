from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.paymentfileupload_file_create_payments_response_status import (
    PaymentfileuploadFileCreatePaymentsResponseStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentfileuploadFileCreatePaymentsResponse")


@attr.s(auto_attribs=True)
class PaymentfileuploadFileCreatePaymentsResponse:
    """File create payments response

    Attributes:
        batch_payment_id (str): Unique id for the Batch Payment Example: B1100001.
        file_id (str): Unique id of the uploaded file Example: F1100001.
        status (PaymentfileuploadFileCreatePaymentsResponseStatus): Status of the uploaded file Example: INVALID.
        file_name (Union[Unset, str]): File name of the uploaded file Example: file1.
    """

    batch_payment_id: str
    file_id: str
    status: PaymentfileuploadFileCreatePaymentsResponseStatus
    file_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        batch_payment_id = self.batch_payment_id
        file_id = self.file_id
        status = self.status.value

        file_name = self.file_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batchPaymentId": batch_payment_id,
                "fileId": file_id,
                "status": status,
            }
        )
        if file_name is not UNSET:
            field_dict["fileName"] = file_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_payment_id = d.pop("batchPaymentId")

        file_id = d.pop("fileId")

        status = PaymentfileuploadFileCreatePaymentsResponseStatus(d.pop("status"))

        file_name = d.pop("fileName", UNSET)

        paymentfileupload_file_create_payments_response = cls(
            batch_payment_id=batch_payment_id,
            file_id=file_id,
            status=status,
            file_name=file_name,
        )

        paymentfileupload_file_create_payments_response.additional_properties = d
        return paymentfileupload_file_create_payments_response

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
