import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.directdebit_mandate_status import DirectdebitMandateStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.directdebit_address import DirectdebitAddress


T = TypeVar("T", bound="DirectdebitMandate")


@attr.s(auto_attribs=True)
class DirectdebitMandate:
    """
    Attributes:
        account_id (str): Unique id for account for this mandate. Example: A0000001.
        account_number (str): Account Number for which direct-debit-mandate has been created. Example: 87654321.
        created_date (datetime.datetime): Datetime when direct-debit-mandate was created.Format is 'yyyy-MM-
            dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        external_reference (str): External reference that was used during creation (appears on the bank statement).
        id (str): Unique id for direct-debit-mandate. Example: G0000001.
        next_valid_collection_date (str): The earliest date a collection can be created. Format is yyyy-MM-dd. Example:
            2018-01-10.
        reference (str): DDI reference that was used during creation.
        sort_code (str): Sort Code of the account for which direct-debit-mandate has been created. Example: 123456.
        status (DirectdebitMandateStatus): Status of the direct-debit-mandate. mandates must be 'ACTIVE' to make
            collections. Can be one of PENDING, SUBMITTED, ACTIVE, SUSPENDED, REJECTED, CANCELLED Example: ACTIVE.
        address_given_on_mandate (Union[Unset, DirectdebitAddress]):
        name_given_on_mandate (Union[Unset, str]):
        payee_account_bid (Union[Unset, str]): Unique id for individual recipient account used for internal transfers
            Example: A0000001.
    """

    account_id: str
    account_number: str
    created_date: datetime.datetime
    external_reference: str
    id: str
    next_valid_collection_date: str
    reference: str
    sort_code: str
    status: DirectdebitMandateStatus
    address_given_on_mandate: Union[Unset, "DirectdebitAddress"] = UNSET
    name_given_on_mandate: Union[Unset, str] = UNSET
    payee_account_bid: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        account_number = self.account_number
        created_date = self.created_date.isoformat()

        external_reference = self.external_reference
        id = self.id
        next_valid_collection_date = self.next_valid_collection_date
        reference = self.reference
        sort_code = self.sort_code
        status = self.status.value

        address_given_on_mandate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address_given_on_mandate, Unset):
            address_given_on_mandate = self.address_given_on_mandate.to_dict()

        name_given_on_mandate = self.name_given_on_mandate
        payee_account_bid = self.payee_account_bid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "accountNumber": account_number,
                "createdDate": created_date,
                "externalReference": external_reference,
                "id": id,
                "nextValidCollectionDate": next_valid_collection_date,
                "reference": reference,
                "sortCode": sort_code,
                "status": status,
            }
        )
        if address_given_on_mandate is not UNSET:
            field_dict["Address given on Mandate"] = address_given_on_mandate
        if name_given_on_mandate is not UNSET:
            field_dict["Name given on Mandate"] = name_given_on_mandate
        if payee_account_bid is not UNSET:
            field_dict["payeeAccountBid"] = payee_account_bid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.directdebit_address import DirectdebitAddress

        d = src_dict.copy()
        account_id = d.pop("accountId")

        account_number = d.pop("accountNumber")

        created_date = isoparse(d.pop("createdDate"))

        external_reference = d.pop("externalReference")

        id = d.pop("id")

        next_valid_collection_date = d.pop("nextValidCollectionDate")

        reference = d.pop("reference")

        sort_code = d.pop("sortCode")

        status = DirectdebitMandateStatus(d.pop("status"))

        _address_given_on_mandate = d.pop("Address given on Mandate", UNSET)
        address_given_on_mandate: Union[Unset, DirectdebitAddress]
        if isinstance(_address_given_on_mandate, Unset):
            address_given_on_mandate = UNSET
        else:
            address_given_on_mandate = DirectdebitAddress.from_dict(_address_given_on_mandate)

        name_given_on_mandate = d.pop("Name given on Mandate", UNSET)

        payee_account_bid = d.pop("payeeAccountBid", UNSET)

        directdebit_mandate = cls(
            account_id=account_id,
            account_number=account_number,
            created_date=created_date,
            external_reference=external_reference,
            id=id,
            next_valid_collection_date=next_valid_collection_date,
            reference=reference,
            sort_code=sort_code,
            status=status,
            address_given_on_mandate=address_given_on_mandate,
            name_given_on_mandate=name_given_on_mandate,
            payee_account_bid=payee_account_bid,
        )

        directdebit_mandate.additional_properties = d
        return directdebit_mandate

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
