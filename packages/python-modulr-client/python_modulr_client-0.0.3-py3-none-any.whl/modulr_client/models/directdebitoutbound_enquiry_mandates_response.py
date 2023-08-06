from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.directdebitoutbound_enquiry_mandate_response import (
        DirectdebitoutboundEnquiryMandateResponse,
    )


T = TypeVar("T", bound="DirectdebitoutboundEnquiryMandatesResponse")


@attr.s(auto_attribs=True)
class DirectdebitoutboundEnquiryMandatesResponse:
    """
    Attributes:
        account_id (str): Account Id
        mandates_list (List['DirectdebitoutboundEnquiryMandateResponse']): List of Mandates
    """

    account_id: str
    mandates_list: List["DirectdebitoutboundEnquiryMandateResponse"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        mandates_list = []
        for mandates_list_item_data in self.mandates_list:
            mandates_list_item = mandates_list_item_data.to_dict()

            mandates_list.append(mandates_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "mandatesList": mandates_list,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.directdebitoutbound_enquiry_mandate_response import (
            DirectdebitoutboundEnquiryMandateResponse,
        )

        d = src_dict.copy()
        account_id = d.pop("accountId")

        mandates_list = []
        _mandates_list = d.pop("mandatesList")
        for mandates_list_item_data in _mandates_list:
            mandates_list_item = DirectdebitoutboundEnquiryMandateResponse.from_dict(
                mandates_list_item_data
            )

            mandates_list.append(mandates_list_item)

        directdebitoutbound_enquiry_mandates_response = cls(
            account_id=account_id,
            mandates_list=mandates_list,
        )

        directdebitoutbound_enquiry_mandates_response.additional_properties = d
        return directdebitoutbound_enquiry_mandates_response

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
