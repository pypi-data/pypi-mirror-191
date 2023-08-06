from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.directdebit_address import DirectdebitAddress


T = TypeVar("T", bound="DirectdebitCreateMandateRequest")


@attr.s(auto_attribs=True)
class DirectdebitCreateMandateRequest:
    """Details of the Direct Debit mandate.

    Attributes:
        account_name (str): Payee's account name
        account_number (str): Payee's account number for which direct-debit-mandate has to be created. Example:
            12345678.
        address (DirectdebitAddress):
        external_reference (str): External reference for mandate
        name (str): Name for mandate
        phone (str): Payee's phone number
        reference (str): Mandate reference, should contain only letters, numbers, space, dot, ampersand, forward-slash
            and hyphen Example: REFER-1.2.
        sort_code (str): Payee's sort code of account for which direct-debit-mandate has to be created. Example: 000000.
        email (Union[Unset, str]): Payee's email address
        payee_account_bid (Union[Unset, str]): Payee's accountBid
    """

    account_name: str
    account_number: str
    address: "DirectdebitAddress"
    external_reference: str
    name: str
    phone: str
    reference: str
    sort_code: str
    email: Union[Unset, str] = UNSET
    payee_account_bid: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_name = self.account_name
        account_number = self.account_number
        address = self.address.to_dict()

        external_reference = self.external_reference
        name = self.name
        phone = self.phone
        reference = self.reference
        sort_code = self.sort_code
        email = self.email
        payee_account_bid = self.payee_account_bid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountName": account_name,
                "accountNumber": account_number,
                "address": address,
                "externalReference": external_reference,
                "name": name,
                "phone": phone,
                "reference": reference,
                "sortCode": sort_code,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if payee_account_bid is not UNSET:
            field_dict["payeeAccountBid"] = payee_account_bid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.directdebit_address import DirectdebitAddress

        d = src_dict.copy()
        account_name = d.pop("accountName")

        account_number = d.pop("accountNumber")

        address = DirectdebitAddress.from_dict(d.pop("address"))

        external_reference = d.pop("externalReference")

        name = d.pop("name")

        phone = d.pop("phone")

        reference = d.pop("reference")

        sort_code = d.pop("sortCode")

        email = d.pop("email", UNSET)

        payee_account_bid = d.pop("payeeAccountBid", UNSET)

        directdebit_create_mandate_request = cls(
            account_name=account_name,
            account_number=account_number,
            address=address,
            external_reference=external_reference,
            name=name,
            phone=phone,
            reference=reference,
            sort_code=sort_code,
            email=email,
            payee_account_bid=payee_account_bid,
        )

        directdebit_create_mandate_request.additional_properties = d
        return directdebit_create_mandate_request

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
