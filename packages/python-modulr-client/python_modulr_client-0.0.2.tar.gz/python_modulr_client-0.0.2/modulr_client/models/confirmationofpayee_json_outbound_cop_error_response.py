from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfirmationofpayeeJsonOutboundCopErrorResponse")


@attr.s(auto_attribs=True)
class ConfirmationofpayeeJsonOutboundCopErrorResponse:
    """Account Name Check Error Response

    Attributes:
        code (str):
        message (str):
        error_code (Union[Unset, str]):
        field (Union[Unset, str]):
        id (Union[Unset, str]):
        source_service (Union[Unset, str]):
    """

    code: str
    message: str
    error_code: Union[Unset, str] = UNSET
    field: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    source_service: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        message = self.message
        error_code = self.error_code
        field = self.field
        id = self.id
        source_service = self.source_service

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if field is not UNSET:
            field_dict["field"] = field
        if id is not UNSET:
            field_dict["id"] = id
        if source_service is not UNSET:
            field_dict["sourceService"] = source_service

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        message = d.pop("message")

        error_code = d.pop("errorCode", UNSET)

        field = d.pop("field", UNSET)

        id = d.pop("id", UNSET)

        source_service = d.pop("sourceService", UNSET)

        confirmationofpayee_json_outbound_cop_error_response = cls(
            code=code,
            message=message,
            error_code=error_code,
            field=field,
            id=id,
            source_service=source_service,
        )

        confirmationofpayee_json_outbound_cop_error_response.additional_properties = d
        return confirmationofpayee_json_outbound_cop_error_response

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
