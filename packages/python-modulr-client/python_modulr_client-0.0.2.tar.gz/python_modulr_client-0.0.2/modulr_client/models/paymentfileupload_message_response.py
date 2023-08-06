from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.paymentfileupload_message_response_code import (
    PaymentfileuploadMessageResponseCode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentfileuploadMessageResponse")


@attr.s(auto_attribs=True)
class PaymentfileuploadMessageResponse:
    """
    Attributes:
        code (Union[Unset, PaymentfileuploadMessageResponseCode]):
        error_code (Union[Unset, str]):
        field (Union[Unset, str]):
        message (Union[Unset, str]):
        source_service (Union[Unset, str]):
    """

    code: Union[Unset, PaymentfileuploadMessageResponseCode] = UNSET
    error_code: Union[Unset, str] = UNSET
    field: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    source_service: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code: Union[Unset, str] = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        error_code = self.error_code
        field = self.field
        message = self.message
        source_service = self.source_service

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if field is not UNSET:
            field_dict["field"] = field
        if message is not UNSET:
            field_dict["message"] = message
        if source_service is not UNSET:
            field_dict["sourceService"] = source_service

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _code = d.pop("code", UNSET)
        code: Union[Unset, PaymentfileuploadMessageResponseCode]
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = PaymentfileuploadMessageResponseCode(_code)

        error_code = d.pop("errorCode", UNSET)

        field = d.pop("field", UNSET)

        message = d.pop("message", UNSET)

        source_service = d.pop("sourceService", UNSET)

        paymentfileupload_message_response = cls(
            code=code,
            error_code=error_code,
            field=field,
            message=message,
            source_service=source_service,
        )

        paymentfileupload_message_response.additional_properties = d
        return paymentfileupload_message_response

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
