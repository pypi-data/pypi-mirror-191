from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_destination import PaymentDestination
    from ..models.payment_poo_details import PaymentPOODetails
    from ..models.payment_regulatory_reporting import PaymentRegulatoryReporting


T = TypeVar("T", bound="PaymentPaymentOutRequest")


@attr.s(auto_attribs=True)
class PaymentPaymentOutRequest:
    """Details of Payment request

    Attributes:
        source_account_id (str): Identifier for the sending Account.
        amount (Union[Unset, float]): Amount of the payment in Major Current Units - '1' = 1.00 GBP Example: 100.
        currency (Union[Unset, str]): Currency of the account in ISO 4217 format. Default is GBP Example: GBP.
        destination (Union[Unset, PaymentDestination]): Destination of the Payment
        end_to_end_reference (Union[Unset, str]): End to end reference. Optional. Example: aReference_00001.
        external_reference (Union[Unset, str]): Your reference for this payment Example: aReference_00001.
        fx_quote_id (Union[Unset, str]): FX quote ID related to this payment. If supplied, neither 'amount' nor
            'currency' should be supplied. Example: Q0000001.
        overseas_payment_detail (Union[Unset, PaymentPOODetails]): Details relating to payment originated overseas
        payment_date (Union[Unset, str]): The future date on which to make the payment. Date format 'yyyy-MM-dd'
            Example: 2017-01-28.
        reference (Union[Unset, str]): Reference to be used for the Payment. This will appear on the Account
            statement/the recipient's bank account. Min 6 to max 18 characters that are not all the same (up to 140
            characters for currencies other than GBP). Can contain alphanumeric, '-', '.', '&', '/' and space. Example:
            Salary.
        regulatory_reporting (Union[Unset, PaymentRegulatoryReporting]): Regulatory reporting
    """

    source_account_id: str
    amount: Union[Unset, float] = UNSET
    currency: Union[Unset, str] = UNSET
    destination: Union[Unset, "PaymentDestination"] = UNSET
    end_to_end_reference: Union[Unset, str] = UNSET
    external_reference: Union[Unset, str] = UNSET
    fx_quote_id: Union[Unset, str] = UNSET
    overseas_payment_detail: Union[Unset, "PaymentPOODetails"] = UNSET
    payment_date: Union[Unset, str] = UNSET
    reference: Union[Unset, str] = UNSET
    regulatory_reporting: Union[Unset, "PaymentRegulatoryReporting"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source_account_id = self.source_account_id
        amount = self.amount
        currency = self.currency
        destination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.destination, Unset):
            destination = self.destination.to_dict()

        end_to_end_reference = self.end_to_end_reference
        external_reference = self.external_reference
        fx_quote_id = self.fx_quote_id
        overseas_payment_detail: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.overseas_payment_detail, Unset):
            overseas_payment_detail = self.overseas_payment_detail.to_dict()

        payment_date = self.payment_date
        reference = self.reference
        regulatory_reporting: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.regulatory_reporting, Unset):
            regulatory_reporting = self.regulatory_reporting.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sourceAccountId": source_account_id,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if destination is not UNSET:
            field_dict["destination"] = destination
        if end_to_end_reference is not UNSET:
            field_dict["endToEndReference"] = end_to_end_reference
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if fx_quote_id is not UNSET:
            field_dict["fxQuoteId"] = fx_quote_id
        if overseas_payment_detail is not UNSET:
            field_dict["overseasPaymentDetail"] = overseas_payment_detail
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
        if reference is not UNSET:
            field_dict["reference"] = reference
        if regulatory_reporting is not UNSET:
            field_dict["regulatoryReporting"] = regulatory_reporting

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_destination import PaymentDestination
        from ..models.payment_poo_details import PaymentPOODetails
        from ..models.payment_regulatory_reporting import PaymentRegulatoryReporting

        d = src_dict.copy()
        source_account_id = d.pop("sourceAccountId")

        amount = d.pop("amount", UNSET)

        currency = d.pop("currency", UNSET)

        _destination = d.pop("destination", UNSET)
        destination: Union[Unset, PaymentDestination]
        if isinstance(_destination, Unset):
            destination = UNSET
        else:
            destination = PaymentDestination.from_dict(_destination)

        end_to_end_reference = d.pop("endToEndReference", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        fx_quote_id = d.pop("fxQuoteId", UNSET)

        _overseas_payment_detail = d.pop("overseasPaymentDetail", UNSET)
        overseas_payment_detail: Union[Unset, PaymentPOODetails]
        if isinstance(_overseas_payment_detail, Unset):
            overseas_payment_detail = UNSET
        else:
            overseas_payment_detail = PaymentPOODetails.from_dict(_overseas_payment_detail)

        payment_date = d.pop("paymentDate", UNSET)

        reference = d.pop("reference", UNSET)

        _regulatory_reporting = d.pop("regulatoryReporting", UNSET)
        regulatory_reporting: Union[Unset, PaymentRegulatoryReporting]
        if isinstance(_regulatory_reporting, Unset):
            regulatory_reporting = UNSET
        else:
            regulatory_reporting = PaymentRegulatoryReporting.from_dict(_regulatory_reporting)

        payment_payment_out_request = cls(
            source_account_id=source_account_id,
            amount=amount,
            currency=currency,
            destination=destination,
            end_to_end_reference=end_to_end_reference,
            external_reference=external_reference,
            fx_quote_id=fx_quote_id,
            overseas_payment_detail=overseas_payment_detail,
            payment_date=payment_date,
            reference=reference,
            regulatory_reporting=regulatory_reporting,
        )

        payment_payment_out_request.additional_properties = d
        return payment_payment_out_request

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
