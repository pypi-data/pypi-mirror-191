from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.paymentfileupload_file_upload_status_response_status import (
    PaymentfileuploadFileUploadStatusResponseStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.paymentfileupload_error_message_response import (
        PaymentfileuploadErrorMessageResponse,
    )


T = TypeVar("T", bound="PaymentfileuploadFileUploadStatusResponse")


@attr.s(auto_attribs=True)
class PaymentfileuploadFileUploadStatusResponse:
    """File upload Status Response

    Attributes:
        status (PaymentfileuploadFileUploadStatusResponseStatus): Status of the uploaded file Example: INVALID.
        errors (Union[Unset, List['PaymentfileuploadErrorMessageResponse']]): If invalid holds the validation errors
            Example: ['Failed parsing'].
        file_name (Union[Unset, str]): File name of the uploaded file Example: file1.
        num_transactions (Union[Unset, int]): Total number of transactions within file Example: 1000.
        total_amount (Union[Unset, float]): Sum of all transaction's amount within file Example: 1539.81.
    """

    status: PaymentfileuploadFileUploadStatusResponseStatus
    errors: Union[Unset, List["PaymentfileuploadErrorMessageResponse"]] = UNSET
    file_name: Union[Unset, str] = UNSET
    num_transactions: Union[Unset, int] = UNSET
    total_amount: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        file_name = self.file_name
        num_transactions = self.num_transactions
        total_amount = self.total_amount

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if errors is not UNSET:
            field_dict["errors"] = errors
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if num_transactions is not UNSET:
            field_dict["numTransactions"] = num_transactions
        if total_amount is not UNSET:
            field_dict["totalAmount"] = total_amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.paymentfileupload_error_message_response import (
            PaymentfileuploadErrorMessageResponse,
        )

        d = src_dict.copy()
        status = PaymentfileuploadFileUploadStatusResponseStatus(d.pop("status"))

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = PaymentfileuploadErrorMessageResponse.from_dict(errors_item_data)

            errors.append(errors_item)

        file_name = d.pop("fileName", UNSET)

        num_transactions = d.pop("numTransactions", UNSET)

        total_amount = d.pop("totalAmount", UNSET)

        paymentfileupload_file_upload_status_response = cls(
            status=status,
            errors=errors,
            file_name=file_name,
            num_transactions=num_transactions,
            total_amount=total_amount,
        )

        paymentfileupload_file_upload_status_response.additional_properties = d
        return paymentfileupload_file_upload_status_response

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
