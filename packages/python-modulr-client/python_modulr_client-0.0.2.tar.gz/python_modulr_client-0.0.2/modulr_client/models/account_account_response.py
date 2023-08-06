import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.account_account_response_status import AccountAccountResponseStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_identifier_response import AccountIdentifierResponse


T = TypeVar("T", bound="AccountAccountResponse")


@attr.s(auto_attribs=True)
class AccountAccountResponse:
    """Account

    Attributes:
        available_balance (str): The current available balance of the Account. Calculated by subtracting any pending
            payments from the current balance Example: 10000.0.
        balance (str): Balance of the account in format 'NN.NN' Example: 10000.0.
        created_date (datetime.datetime): Datetime when the account was created. Format is 'yyyy-MM-dd'T'HH:mm:ssZ'
            where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        currency (str): Currency of the account in ISO 4217 format Example: GBP.
        customer_id (str): Unique id of the Customer Example: C0000001.
        id (str): Unique id for the account Example: A0000001.
        identifiers (List['AccountIdentifierResponse']):
        name (str): Name for the account
        status (AccountAccountResponseStatus): Status of the account. Accounts must be 'ACTIVE' to make and receive
            payments. Can be one of ACTIVE, BLOCKED, CLOSED, CLIENT_BLOCKED Example: ACTIVE.
        access_groups (Union[Unset, List[str]]): Ids of Access Groups this account belongs to
        customer_name (Union[Unset, str]): Customer Name
        direct_debit (Union[Unset, bool]): Direct Debit Enabled
        external_reference (Union[Unset, str]): Your reference for an account Example: aReference_00001.
    """

    available_balance: str
    balance: str
    created_date: datetime.datetime
    currency: str
    customer_id: str
    id: str
    identifiers: List["AccountIdentifierResponse"]
    name: str
    status: AccountAccountResponseStatus
    access_groups: Union[Unset, List[str]] = UNSET
    customer_name: Union[Unset, str] = UNSET
    direct_debit: Union[Unset, bool] = UNSET
    external_reference: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        available_balance = self.available_balance
        balance = self.balance
        created_date = self.created_date.isoformat()

        currency = self.currency
        customer_id = self.customer_id
        id = self.id
        identifiers = []
        for identifiers_item_data in self.identifiers:
            identifiers_item = identifiers_item_data.to_dict()

            identifiers.append(identifiers_item)

        name = self.name
        status = self.status.value

        access_groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.access_groups, Unset):
            access_groups = self.access_groups

        customer_name = self.customer_name
        direct_debit = self.direct_debit
        external_reference = self.external_reference

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "availableBalance": available_balance,
                "balance": balance,
                "createdDate": created_date,
                "currency": currency,
                "customerId": customer_id,
                "id": id,
                "identifiers": identifiers,
                "name": name,
                "status": status,
            }
        )
        if access_groups is not UNSET:
            field_dict["accessGroups"] = access_groups
        if customer_name is not UNSET:
            field_dict["customerName"] = customer_name
        if direct_debit is not UNSET:
            field_dict["directDebit"] = direct_debit
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_identifier_response import AccountIdentifierResponse

        d = src_dict.copy()
        available_balance = d.pop("availableBalance")

        balance = d.pop("balance")

        created_date = isoparse(d.pop("createdDate"))

        currency = d.pop("currency")

        customer_id = d.pop("customerId")

        id = d.pop("id")

        identifiers = []
        _identifiers = d.pop("identifiers")
        for identifiers_item_data in _identifiers:
            identifiers_item = AccountIdentifierResponse.from_dict(identifiers_item_data)

            identifiers.append(identifiers_item)

        name = d.pop("name")

        status = AccountAccountResponseStatus(d.pop("status"))

        access_groups = cast(List[str], d.pop("accessGroups", UNSET))

        customer_name = d.pop("customerName", UNSET)

        direct_debit = d.pop("directDebit", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        account_account_response = cls(
            available_balance=available_balance,
            balance=balance,
            created_date=created_date,
            currency=currency,
            customer_id=customer_id,
            id=id,
            identifiers=identifiers,
            name=name,
            status=status,
            access_groups=access_groups,
            customer_name=customer_name,
            direct_debit=direct_debit,
            external_reference=external_reference,
        )

        account_account_response.additional_properties = d
        return account_account_response

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
