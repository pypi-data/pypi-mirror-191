from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_request import AccountAddressRequest
    from ..models.account_customer_trust_request import AccountCustomerTrustRequest
    from ..models.account_update_associate_request import AccountUpdateAssociateRequest
    from ..models.account_update_brand_name_request import AccountUpdateBrandNameRequest


T = TypeVar("T", bound="AccountUpdateCustomerRequest")


@attr.s(auto_attribs=True)
class AccountUpdateCustomerRequest:
    r"""Details of customer to edit

    Attributes:
        associates (Union[Unset, List['AccountUpdateAssociateRequest']]): Applicable to all types except 'PCM_BUSINESS'
        brand_names (Union[Unset, List['AccountUpdateBrandNameRequest']]): The customers brand name(s)
        customer_trust (Union[Unset, AccountCustomerTrustRequest]): Trust nature for customers of type Trust. Mandatory
            for type Trust, not to be set for non-trust customers.
        external_reference (Union[Unset, str]): External Reference can only have alphanumeric characters plus
            underscore, hyphen and space up to 50 characters long
        name (Union[Unset, str]): AlphaNumeric characters plus [ _ ' @ , & £ $ € ¥ = # % ‘ ’ : ; \ / < > « »  ! ‘ “ ” .
            ? - *{ }  + % ( )]. Mandatory for all types except 'INDIVIDUAL and PCM_INDIVIDUAL'
        trading_address (Union[Unset, AccountAddressRequest]): Applicable to all types except 'INDIVIDUAL' and
            'PCM_INDIVIDUAL'
    """

    associates: Union[Unset, List["AccountUpdateAssociateRequest"]] = UNSET
    brand_names: Union[Unset, List["AccountUpdateBrandNameRequest"]] = UNSET
    customer_trust: Union[Unset, "AccountCustomerTrustRequest"] = UNSET
    external_reference: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    trading_address: Union[Unset, "AccountAddressRequest"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        associates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.associates, Unset):
            associates = []
            for associates_item_data in self.associates:
                associates_item = associates_item_data.to_dict()

                associates.append(associates_item)

        brand_names: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.brand_names, Unset):
            brand_names = []
            for brand_names_item_data in self.brand_names:
                brand_names_item = brand_names_item_data.to_dict()

                brand_names.append(brand_names_item)

        customer_trust: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.customer_trust, Unset):
            customer_trust = self.customer_trust.to_dict()

        external_reference = self.external_reference
        name = self.name
        trading_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trading_address, Unset):
            trading_address = self.trading_address.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if associates is not UNSET:
            field_dict["associates"] = associates
        if brand_names is not UNSET:
            field_dict["brandNames"] = brand_names
        if customer_trust is not UNSET:
            field_dict["customerTrust"] = customer_trust
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if name is not UNSET:
            field_dict["name"] = name
        if trading_address is not UNSET:
            field_dict["tradingAddress"] = trading_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_address_request import AccountAddressRequest
        from ..models.account_customer_trust_request import AccountCustomerTrustRequest
        from ..models.account_update_associate_request import (
            AccountUpdateAssociateRequest,
        )
        from ..models.account_update_brand_name_request import (
            AccountUpdateBrandNameRequest,
        )

        d = src_dict.copy()
        associates = []
        _associates = d.pop("associates", UNSET)
        for associates_item_data in _associates or []:
            associates_item = AccountUpdateAssociateRequest.from_dict(associates_item_data)

            associates.append(associates_item)

        brand_names = []
        _brand_names = d.pop("brandNames", UNSET)
        for brand_names_item_data in _brand_names or []:
            brand_names_item = AccountUpdateBrandNameRequest.from_dict(brand_names_item_data)

            brand_names.append(brand_names_item)

        _customer_trust = d.pop("customerTrust", UNSET)
        customer_trust: Union[Unset, AccountCustomerTrustRequest]
        if isinstance(_customer_trust, Unset):
            customer_trust = UNSET
        else:
            customer_trust = AccountCustomerTrustRequest.from_dict(_customer_trust)

        external_reference = d.pop("externalReference", UNSET)

        name = d.pop("name", UNSET)

        _trading_address = d.pop("tradingAddress", UNSET)
        trading_address: Union[Unset, AccountAddressRequest]
        if isinstance(_trading_address, Unset):
            trading_address = UNSET
        else:
            trading_address = AccountAddressRequest.from_dict(_trading_address)

        account_update_customer_request = cls(
            associates=associates,
            brand_names=brand_names,
            customer_trust=customer_trust,
            external_reference=external_reference,
            name=name,
            trading_address=trading_address,
        )

        account_update_customer_request.additional_properties = d
        return account_update_customer_request

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
