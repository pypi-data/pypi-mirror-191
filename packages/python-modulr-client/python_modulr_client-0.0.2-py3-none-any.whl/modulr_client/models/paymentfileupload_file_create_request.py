from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentfileuploadFileCreateRequest")


@attr.s(auto_attribs=True)
class PaymentfileuploadFileCreateRequest:
    """File create payments request body

    Attributes:
        use_duplicate (Union[Unset, bool]): User confirms to proceed with creating payments on a duplicate file
    """

    use_duplicate: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        use_duplicate = self.use_duplicate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if use_duplicate is not UNSET:
            field_dict["useDuplicate"] = use_duplicate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        use_duplicate = d.pop("useDuplicate", UNSET)

        paymentfileupload_file_create_request = cls(
            use_duplicate=use_duplicate,
        )

        paymentfileupload_file_create_request.additional_properties = d
        return paymentfileupload_file_create_request

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
