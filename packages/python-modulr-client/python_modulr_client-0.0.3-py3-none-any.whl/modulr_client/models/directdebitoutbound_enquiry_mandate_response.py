from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.directdebitoutbound_enquiry_mandate_response_auddis_indicator import (
    DirectdebitoutboundEnquiryMandateResponseAuddisIndicator,
)

T = TypeVar("T", bound="DirectdebitoutboundEnquiryMandateResponse")


@attr.s(auto_attribs=True)
class DirectdebitoutboundEnquiryMandateResponse:
    """List of Mandates

    Attributes:
        auddis_indicator (DirectdebitoutboundEnquiryMandateResponseAuddisIndicator): AUDDIS Flag (AUDDIS / Non-AUDDIS)
        mandate_id (str): Mandate Id
        mandate_reference (str): Mandate Reference
        mandate_status (str): Status
        merchant_account_number (str): Merchant Account Number
        merchant_name (str): Merchant Name
        merchant_number (str): Merchant Number
        merchant_sort_code (str): Merchant Sort Code
        setup_date (str): Setup date
    """

    auddis_indicator: DirectdebitoutboundEnquiryMandateResponseAuddisIndicator
    mandate_id: str
    mandate_reference: str
    mandate_status: str
    merchant_account_number: str
    merchant_name: str
    merchant_number: str
    merchant_sort_code: str
    setup_date: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auddis_indicator = self.auddis_indicator.value

        mandate_id = self.mandate_id
        mandate_reference = self.mandate_reference
        mandate_status = self.mandate_status
        merchant_account_number = self.merchant_account_number
        merchant_name = self.merchant_name
        merchant_number = self.merchant_number
        merchant_sort_code = self.merchant_sort_code
        setup_date = self.setup_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auddisIndicator": auddis_indicator,
                "mandateId": mandate_id,
                "mandateReference": mandate_reference,
                "mandateStatus": mandate_status,
                "merchantAccountNumber": merchant_account_number,
                "merchantName": merchant_name,
                "merchantNumber": merchant_number,
                "merchantSortCode": merchant_sort_code,
                "setupDate": setup_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        auddis_indicator = DirectdebitoutboundEnquiryMandateResponseAuddisIndicator(
            d.pop("auddisIndicator")
        )

        mandate_id = d.pop("mandateId")

        mandate_reference = d.pop("mandateReference")

        mandate_status = d.pop("mandateStatus")

        merchant_account_number = d.pop("merchantAccountNumber")

        merchant_name = d.pop("merchantName")

        merchant_number = d.pop("merchantNumber")

        merchant_sort_code = d.pop("merchantSortCode")

        setup_date = d.pop("setupDate")

        directdebitoutbound_enquiry_mandate_response = cls(
            auddis_indicator=auddis_indicator,
            mandate_id=mandate_id,
            mandate_reference=mandate_reference,
            mandate_status=mandate_status,
            merchant_account_number=merchant_account_number,
            merchant_name=merchant_name,
            merchant_number=merchant_number,
            merchant_sort_code=merchant_sort_code,
            setup_date=setup_date,
        )

        directdebitoutbound_enquiry_mandate_response.additional_properties = d
        return directdebitoutbound_enquiry_mandate_response

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
