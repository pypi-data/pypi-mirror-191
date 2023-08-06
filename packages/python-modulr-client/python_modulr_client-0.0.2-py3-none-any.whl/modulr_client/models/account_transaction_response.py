import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.account_transaction_response_type import AccountTransactionResponseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_account_response import AccountAccountResponse
    from ..models.account_transaction_response_additional_info import (
        AccountTransactionResponseAdditionalInfo,
    )


T = TypeVar("T", bound="AccountTransactionResponse")


@attr.s(auto_attribs=True)
class AccountTransactionResponse:
    """Transaction

    Attributes:
        amount (float): Amount of the transaction in Major Currency Units
        credit (bool): Indicates if the transaction was a Credit or a Debit
        currency (str): Currency of the account in ISO 4217 format Example: GBP.
        id (str): Unique id for the Transaction Example: T0000001.
        posted_date (datetime.datetime): Datetime when the transaction was posted to the Modulr system. Format is 'yyyy-
            MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        source_id (str):
        transaction_date (datetime.datetime): Datetime when the transaction took place. Format is 'yyyy-MM-
            dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        type (AccountTransactionResponseType): Enumerated type indicating the type of the transaction
        account (Union[Unset, AccountAccountResponse]): Account
        additional_info (Union[Unset, AccountTransactionResponseAdditionalInfo]): any extra information available on
            transaction.
        description (Union[Unset, str]): Description of the transaction. Contains Payer/ Payee details and reference
        source_external_reference (Union[Unset, str]):
    """

    amount: float
    credit: bool
    currency: str
    id: str
    posted_date: datetime.datetime
    source_id: str
    transaction_date: datetime.datetime
    type: AccountTransactionResponseType
    account: Union[Unset, "AccountAccountResponse"] = UNSET
    additional_info: Union[Unset, "AccountTransactionResponseAdditionalInfo"] = UNSET
    description: Union[Unset, str] = UNSET
    source_external_reference: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        credit = self.credit
        currency = self.currency
        id = self.id
        posted_date = self.posted_date.isoformat()

        source_id = self.source_id
        transaction_date = self.transaction_date.isoformat()

        type = self.type.value

        account: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        additional_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.additional_info, Unset):
            additional_info = self.additional_info.to_dict()

        description = self.description
        source_external_reference = self.source_external_reference

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "credit": credit,
                "currency": currency,
                "id": id,
                "postedDate": posted_date,
                "sourceId": source_id,
                "transactionDate": transaction_date,
                "type": type,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if additional_info is not UNSET:
            field_dict["additionalInfo"] = additional_info
        if description is not UNSET:
            field_dict["description"] = description
        if source_external_reference is not UNSET:
            field_dict["sourceExternalReference"] = source_external_reference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_account_response import AccountAccountResponse
        from ..models.account_transaction_response_additional_info import (
            AccountTransactionResponseAdditionalInfo,
        )

        d = src_dict.copy()
        amount = d.pop("amount")

        credit = d.pop("credit")

        currency = d.pop("currency")

        id = d.pop("id")

        posted_date = isoparse(d.pop("postedDate"))

        source_id = d.pop("sourceId")

        transaction_date = isoparse(d.pop("transactionDate"))

        type = AccountTransactionResponseType(d.pop("type"))

        _account = d.pop("account", UNSET)
        account: Union[Unset, AccountAccountResponse]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = AccountAccountResponse.from_dict(_account)

        _additional_info = d.pop("additionalInfo", UNSET)
        additional_info: Union[Unset, AccountTransactionResponseAdditionalInfo]
        if isinstance(_additional_info, Unset):
            additional_info = UNSET
        else:
            additional_info = AccountTransactionResponseAdditionalInfo.from_dict(_additional_info)

        description = d.pop("description", UNSET)

        source_external_reference = d.pop("sourceExternalReference", UNSET)

        account_transaction_response = cls(
            amount=amount,
            credit=credit,
            currency=currency,
            id=id,
            posted_date=posted_date,
            source_id=source_id,
            transaction_date=transaction_date,
            type=type,
            account=account,
            additional_info=additional_info,
            description=description,
            source_external_reference=source_external_reference,
        )

        account_transaction_response.additional_properties = d
        return account_transaction_response

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
