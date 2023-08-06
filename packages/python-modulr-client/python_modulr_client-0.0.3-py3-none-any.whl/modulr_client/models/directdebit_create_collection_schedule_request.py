from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.directdebit_create_collection_schedule_request_currency import (
    DirectdebitCreateCollectionScheduleRequestCurrency,
)
from ..models.directdebit_create_collection_schedule_request_frequency import (
    DirectdebitCreateCollectionScheduleRequestFrequency,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DirectdebitCreateCollectionScheduleRequest")


@attr.s(auto_attribs=True)
class DirectdebitCreateCollectionScheduleRequest:
    """Details of collection to create.

    Attributes:
        currency (DirectdebitCreateCollectionScheduleRequestCurrency): Currency in which payment should be made. Can be
            one of GBP, EUR, AED, AFN, ALL, AMD, ANG, AOA, ARS, AUD, AWG, AZN, BAM, BBD, BDT, BGN, BHD, BIF, BMD, BND, BOB,
            BOV, BRL, BSD, BTN, BWP, BYN, BZD, CAD, CDF, CHE, CHF, CHW, CLF, CLP, CNY, COP, COU, CRC, CUC, CUP, CVE, CZK,
            DJF, DKK, DOP, DZD, EGP, ERN, ETB, FJD, FKP, GEL, GHS, GIP, GMD, GNF, GTQ, GYD, HKD, HNL, HRK, HTG, HUF, IDR,
            ILS, INR, IQD, IRR, ISK, JMD, JOD, JPY, KES, KGS, KHR, KMF, KPW, KRW, KWD, KYD, KZT, LAK, LBP, LKR, LRD, LSL,
            LYD, MAD, MDL, MGA, MKD, MMK, MNT, MOP, MRU, MUR, MVR, MWK, MXN, MXV, MYR, MZN, NAD, NGN, NIO, NOK, NPR, NZD,
            OMR, PAB, PEN, PGK, PHP, PKR, PLN, PYG, QAR, RON, RSD, RUB, RWF, SAR, SBD, SCR, SDG, SEK, SGD, SLE, SLL, SOS,
            SRD, SSP, STN, SVC, SYP, SZL, SHP, THB, TJS, TMT, TND, TOP, TRY, TTD, TWD, TZS, UAH, UGX, USD, USN, UYI, UYU,
            UYW, UZS, VES, VND, VUV, WST, XAF, XAG, XAU, XBA, XBB, XBC, XBD, XCD, XDR, XOF, XPD, XPF, XPT, XSU, XTS, XUA,
            XXX, YER, ZAR, ZMW, ZWL
        frequency (DirectdebitCreateCollectionScheduleRequestFrequency): Frequency for direct-debit collection. Can be
            one of ONCE, MONTHLY, QUARTERLY, SEMI_ANNUALLY, ANNUALLY, WEEKLY, EVERY_TWO_WEEKS, EVERY_FOUR_WEEKS
        number_of_payments (int): Number of payments for direct-debit collection
        external_reference (Union[Unset, str]): External Reference for collection schedule, should contain only
            alphanumeric characters, underscore, hyphen and space. Example: REFERENCE - 12.
        first_payment_amount (Union[Unset, float]): Amount of the first collection payment Example: 100.
        first_payment_date (Union[Unset, str]): Date of the first collection payment. yyyy-MM-dd Example: 2018-01-10.
        regular_payment_amount (Union[Unset, float]): Amount of the regular collection payments Example: 100.
        regular_payment_start_date (Union[Unset, str]): Start date of the regular collection payment. yyyy-MM-dd
            Example: 2018-01-10.
    """

    currency: DirectdebitCreateCollectionScheduleRequestCurrency
    frequency: DirectdebitCreateCollectionScheduleRequestFrequency
    number_of_payments: int
    external_reference: Union[Unset, str] = UNSET
    first_payment_amount: Union[Unset, float] = UNSET
    first_payment_date: Union[Unset, str] = UNSET
    regular_payment_amount: Union[Unset, float] = UNSET
    regular_payment_start_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency = self.currency.value

        frequency = self.frequency.value

        number_of_payments = self.number_of_payments
        external_reference = self.external_reference
        first_payment_amount = self.first_payment_amount
        first_payment_date = self.first_payment_date
        regular_payment_amount = self.regular_payment_amount
        regular_payment_start_date = self.regular_payment_start_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currency": currency,
                "frequency": frequency,
                "numberOfPayments": number_of_payments,
            }
        )
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if first_payment_amount is not UNSET:
            field_dict["firstPaymentAmount"] = first_payment_amount
        if first_payment_date is not UNSET:
            field_dict["firstPaymentDate"] = first_payment_date
        if regular_payment_amount is not UNSET:
            field_dict["regularPaymentAmount"] = regular_payment_amount
        if regular_payment_start_date is not UNSET:
            field_dict["regularPaymentStartDate"] = regular_payment_start_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency = DirectdebitCreateCollectionScheduleRequestCurrency(d.pop("currency"))

        frequency = DirectdebitCreateCollectionScheduleRequestFrequency(d.pop("frequency"))

        number_of_payments = d.pop("numberOfPayments")

        external_reference = d.pop("externalReference", UNSET)

        first_payment_amount = d.pop("firstPaymentAmount", UNSET)

        first_payment_date = d.pop("firstPaymentDate", UNSET)

        regular_payment_amount = d.pop("regularPaymentAmount", UNSET)

        regular_payment_start_date = d.pop("regularPaymentStartDate", UNSET)

        directdebit_create_collection_schedule_request = cls(
            currency=currency,
            frequency=frequency,
            number_of_payments=number_of_payments,
            external_reference=external_reference,
            first_payment_amount=first_payment_amount,
            first_payment_date=first_payment_date,
            regular_payment_amount=regular_payment_amount,
            regular_payment_start_date=regular_payment_start_date,
        )

        directdebit_create_collection_schedule_request.additional_properties = d
        return directdebit_create_collection_schedule_request

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
