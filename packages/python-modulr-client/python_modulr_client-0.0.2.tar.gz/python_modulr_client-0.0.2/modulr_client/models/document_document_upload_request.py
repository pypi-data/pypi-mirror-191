from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DocumentDocumentUploadRequest")


@attr.s(auto_attribs=True)
class DocumentDocumentUploadRequest:
    """
    Attributes:
        content (str): Needs to be Base64 encoded
        file_name (str):
        group (str): Use to group documents together. Combination of group+filename should be unique else the files will
            be overwritten
    """

    content: str
    file_name: str
    group: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content
        file_name = self.file_name
        group = self.group

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "fileName": file_name,
                "group": group,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        file_name = d.pop("fileName")

        group = d.pop("group")

        document_document_upload_request = cls(
            content=content,
            file_name=file_name,
            group=group,
        )

        document_document_upload_request.additional_properties = d
        return document_document_upload_request

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
