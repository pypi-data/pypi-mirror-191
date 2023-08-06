from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_create_account_request_currency import (
    AccountCreateAccountRequestCurrency,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_create_account_identifier import (
        AccountCreateAccountIdentifier,
    )


T = TypeVar("T", bound="AccountCreateAccountRequest")


@attr.s(auto_attribs=True)
class AccountCreateAccountRequest:
    """Details of account to create

    Attributes:
        currency (AccountCreateAccountRequestCurrency):
        external_reference (Union[Unset, str]): External Reference can only have alphanumeric characters plus
            underscore, hyphen and space up to 50 characters long
        identifier (Union[Unset, AccountCreateAccountIdentifier]): The identifier to assign to the account. Only
            available to selected partners.
        product_code (Union[Unset, str]): Product associated with the account. Contact your account manager for correct
            code to use.
    """

    currency: AccountCreateAccountRequestCurrency
    external_reference: Union[Unset, str] = UNSET
    identifier: Union[Unset, "AccountCreateAccountIdentifier"] = UNSET
    product_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency = self.currency.value

        external_reference = self.external_reference
        identifier: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.identifier, Unset):
            identifier = self.identifier.to_dict()

        product_code = self.product_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currency": currency,
            }
        )
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if product_code is not UNSET:
            field_dict["productCode"] = product_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_create_account_identifier import (
            AccountCreateAccountIdentifier,
        )

        d = src_dict.copy()
        currency = AccountCreateAccountRequestCurrency(d.pop("currency"))

        external_reference = d.pop("externalReference", UNSET)

        _identifier = d.pop("identifier", UNSET)
        identifier: Union[Unset, AccountCreateAccountIdentifier]
        if isinstance(_identifier, Unset):
            identifier = UNSET
        else:
            identifier = AccountCreateAccountIdentifier.from_dict(_identifier)

        product_code = d.pop("productCode", UNSET)

        account_create_account_request = cls(
            currency=currency,
            external_reference=external_reference,
            identifier=identifier,
            product_code=product_code,
        )

        account_create_account_request.additional_properties = d
        return account_create_account_request

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
