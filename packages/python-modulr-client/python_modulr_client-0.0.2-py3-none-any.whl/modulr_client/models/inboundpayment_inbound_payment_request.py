from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.inboundpayment_inbound_payment_request_type import (
    InboundpaymentInboundPaymentRequestType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inboundpayment_party_detail_request import (
        InboundpaymentPartyDetailRequest,
    )


T = TypeVar("T", bound="InboundpaymentInboundPaymentRequest")


@attr.s(auto_attribs=True)
class InboundpaymentInboundPaymentRequest:
    """Details of credit to the account

    Attributes:
        account_id (str): The account to be credited
        amount (float): Amount of the payment in major current Units - '1' = 1.00 GBP
        description (str): Description of the credit
        payer_detail (InboundpaymentPartyDetailRequest): Payee details
        type (InboundpaymentInboundPaymentRequestType):  Type of credit, values:
        number_of_transactions (Union[Unset, int]): Number of credit transactions to create, defaults to 1
        payee_detail (Union[Unset, InboundpaymentPartyDetailRequest]): Payee details
        transaction_date (Union[Unset, str]): Date of credit in yyyy-MM-ddTHH:mm:ssZ format
    """

    account_id: str
    amount: float
    description: str
    payer_detail: "InboundpaymentPartyDetailRequest"
    type: InboundpaymentInboundPaymentRequestType
    number_of_transactions: Union[Unset, int] = UNSET
    payee_detail: Union[Unset, "InboundpaymentPartyDetailRequest"] = UNSET
    transaction_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        amount = self.amount
        description = self.description
        payer_detail = self.payer_detail.to_dict()

        type = self.type.value

        number_of_transactions = self.number_of_transactions
        payee_detail: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payee_detail, Unset):
            payee_detail = self.payee_detail.to_dict()

        transaction_date = self.transaction_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "amount": amount,
                "description": description,
                "payerDetail": payer_detail,
                "type": type,
            }
        )
        if number_of_transactions is not UNSET:
            field_dict["numberOfTransactions"] = number_of_transactions
        if payee_detail is not UNSET:
            field_dict["payeeDetail"] = payee_detail
        if transaction_date is not UNSET:
            field_dict["transactionDate"] = transaction_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.inboundpayment_party_detail_request import (
            InboundpaymentPartyDetailRequest,
        )

        d = src_dict.copy()
        account_id = d.pop("accountId")

        amount = d.pop("amount")

        description = d.pop("description")

        payer_detail = InboundpaymentPartyDetailRequest.from_dict(d.pop("payerDetail"))

        type = InboundpaymentInboundPaymentRequestType(d.pop("type"))

        number_of_transactions = d.pop("numberOfTransactions", UNSET)

        _payee_detail = d.pop("payeeDetail", UNSET)
        payee_detail: Union[Unset, InboundpaymentPartyDetailRequest]
        if isinstance(_payee_detail, Unset):
            payee_detail = UNSET
        else:
            payee_detail = InboundpaymentPartyDetailRequest.from_dict(_payee_detail)

        transaction_date = d.pop("transactionDate", UNSET)

        inboundpayment_inbound_payment_request = cls(
            account_id=account_id,
            amount=amount,
            description=description,
            payer_detail=payer_detail,
            type=type,
            number_of_transactions=number_of_transactions,
            payee_detail=payee_detail,
            transaction_date=transaction_date,
        )

        inboundpayment_inbound_payment_request.additional_properties = d
        return inboundpayment_inbound_payment_request

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
