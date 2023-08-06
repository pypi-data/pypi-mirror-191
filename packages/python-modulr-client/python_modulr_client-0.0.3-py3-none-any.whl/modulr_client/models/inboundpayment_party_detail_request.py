from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inboundpayment_account_identifier_detail_request import (
        InboundpaymentAccountIdentifierDetailRequest,
    )
    from ..models.inboundpayment_address import InboundpaymentAddress


T = TypeVar("T", bound="InboundpaymentPartyDetailRequest")


@attr.s(auto_attribs=True)
class InboundpaymentPartyDetailRequest:
    """Payee details

    Attributes:
        identifier (InboundpaymentAccountIdentifierDetailRequest): Account identifier
        name (str): Party name
        address (Union[Unset, InboundpaymentAddress]): Party address
    """

    identifier: "InboundpaymentAccountIdentifierDetailRequest"
    name: str
    address: Union[Unset, "InboundpaymentAddress"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier.to_dict()

        name = self.name
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identifier": identifier,
                "name": name,
            }
        )
        if address is not UNSET:
            field_dict["address"] = address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.inboundpayment_account_identifier_detail_request import (
            InboundpaymentAccountIdentifierDetailRequest,
        )
        from ..models.inboundpayment_address import InboundpaymentAddress

        d = src_dict.copy()
        identifier = InboundpaymentAccountIdentifierDetailRequest.from_dict(d.pop("identifier"))

        name = d.pop("name")

        _address = d.pop("address", UNSET)
        address: Union[Unset, InboundpaymentAddress]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = InboundpaymentAddress.from_dict(_address)

        inboundpayment_party_detail_request = cls(
            identifier=identifier,
            name=name,
            address=address,
        )

        inboundpayment_party_detail_request.additional_properties = d
        return inboundpayment_party_detail_request

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
