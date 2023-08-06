import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.account_pending_transaction_response_currency import (
    AccountPendingTransactionResponseCurrency,
)
from ..models.account_pending_transaction_response_type import (
    AccountPendingTransactionResponseType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountPendingTransactionResponse")


@attr.s(auto_attribs=True)
class AccountPendingTransactionResponse:
    """List of responses on the current page

    Attributes:
        account_id (str): Unique id for the Account Example: A0000001.
        amount (float): Amount of the transaction in Major Currency Units
        credit (bool): Indicates if the transaction was a Credit or a Debit
        currency (AccountPendingTransactionResponseCurrency): Currency of the account in ISO 4217 format Example: GBP.
        pending_transaction_id (str): Unique id for the pending transaction Example: T0000001.
        posted_date (datetime.datetime): Datetime when the transaction was posted to the Modulr system. Format is 'yyyy-
            MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        transaction_date (datetime.datetime): Datetime when the transaction took place. Format is 'yyyy-MM-
            dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        type (AccountPendingTransactionResponseType): Enumerated type indicating the type of the transaction
        description (Union[Unset, str]): Description of the transaction. Contains Payer/ Payee details and reference
        source_id (Union[Unset, str]): SourceId of pending transaction Example: C1234567.
        status (Union[Unset, str]): Status of pending transaction Example: PENDING.
    """

    account_id: str
    amount: float
    credit: bool
    currency: AccountPendingTransactionResponseCurrency
    pending_transaction_id: str
    posted_date: datetime.datetime
    transaction_date: datetime.datetime
    type: AccountPendingTransactionResponseType
    description: Union[Unset, str] = UNSET
    source_id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        amount = self.amount
        credit = self.credit
        currency = self.currency.value

        pending_transaction_id = self.pending_transaction_id
        posted_date = self.posted_date.isoformat()

        transaction_date = self.transaction_date.isoformat()

        type = self.type.value

        description = self.description
        source_id = self.source_id
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "amount": amount,
                "credit": credit,
                "currency": currency,
                "pendingTransactionId": pending_transaction_id,
                "postedDate": posted_date,
                "transactionDate": transaction_date,
                "type": type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if source_id is not UNSET:
            field_dict["sourceId"] = source_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("accountId")

        amount = d.pop("amount")

        credit = d.pop("credit")

        currency = AccountPendingTransactionResponseCurrency(d.pop("currency"))

        pending_transaction_id = d.pop("pendingTransactionId")

        posted_date = isoparse(d.pop("postedDate"))

        transaction_date = isoparse(d.pop("transactionDate"))

        type = AccountPendingTransactionResponseType(d.pop("type"))

        description = d.pop("description", UNSET)

        source_id = d.pop("sourceId", UNSET)

        status = d.pop("status", UNSET)

        account_pending_transaction_response = cls(
            account_id=account_id,
            amount=amount,
            credit=credit,
            currency=currency,
            pending_transaction_id=pending_transaction_id,
            posted_date=posted_date,
            transaction_date=transaction_date,
            type=type,
            description=description,
            source_id=source_id,
            status=status,
        )

        account_pending_transaction_response.additional_properties = d
        return account_pending_transaction_response

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
