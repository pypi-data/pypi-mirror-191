from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AccountDocumentInfo")


@attr.s(auto_attribs=True)
class AccountDocumentInfo:
    """Document

    Attributes:
        file_name (str):
        path (str):
        uploaded_date (str): Valid date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000 Example: 2017-01-28T01:01:01+0000.
    """

    file_name: str
    path: str
    uploaded_date: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_name = self.file_name
        path = self.path
        uploaded_date = self.uploaded_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fileName": file_name,
                "path": path,
                "uploadedDate": uploaded_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_name = d.pop("fileName")

        path = d.pop("path")

        uploaded_date = d.pop("uploadedDate")

        account_document_info = cls(
            file_name=file_name,
            path=path,
            uploaded_date=uploaded_date,
        )

        account_document_info.additional_properties = d
        return account_document_info

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
