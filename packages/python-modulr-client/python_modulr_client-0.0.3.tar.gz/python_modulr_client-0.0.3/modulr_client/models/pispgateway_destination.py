from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pispgateway_destination_type import PispgatewayDestinationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PispgatewayDestination")


@attr.s(auto_attribs=True)
class PispgatewayDestination:
    """The destination account for the payment

    Attributes:
        type (PispgatewayDestinationType): Indicates the type of destination. Can be one of ACCOUNT, SCAN
        account_number (Union[Unset, str]): Account Number of destination account if using SCAN type Example: 12345678.
        id (Union[Unset, str]): Identifier of the destination account if using ACCOUNT type Example: A1100001.
        name (Union[Unset, str]): Name of destination account if using SCAN type (this may be truncated) Example: Test.
        sort_code (Union[Unset, str]): Sort Code of destination account if using SCAN type Example: 000000.
    """

    type: PispgatewayDestinationType
    account_number: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    sort_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        account_number = self.account_number
        id = self.id
        name = self.name
        sort_code = self.sort_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if sort_code is not UNSET:
            field_dict["sortCode"] = sort_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = PispgatewayDestinationType(d.pop("type"))

        account_number = d.pop("accountNumber", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        sort_code = d.pop("sortCode", UNSET)

        pispgateway_destination = cls(
            type=type,
            account_number=account_number,
            id=id,
            name=name,
            sort_code=sort_code,
        )

        pispgateway_destination.additional_properties = d
        return pispgateway_destination

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
