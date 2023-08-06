from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PaymentfileuploadFileUploadResponse")


@attr.s(auto_attribs=True)
class PaymentfileuploadFileUploadResponse:
    """
    Attributes:
        file_id (str): Unique id of the uploaded file Example: F1100001.
    """

    file_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fileId": file_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_id = d.pop("fileId")

        paymentfileupload_file_upload_response = cls(
            file_id=file_id,
        )

        paymentfileupload_file_upload_response.additional_properties = d
        return paymentfileupload_file_upload_response

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
