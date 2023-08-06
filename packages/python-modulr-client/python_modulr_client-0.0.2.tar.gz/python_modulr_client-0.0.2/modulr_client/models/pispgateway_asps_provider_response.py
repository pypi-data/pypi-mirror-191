from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pispgateway_capability import PispgatewayCapability


T = TypeVar("T", bound="PispgatewayAspsProviderResponse")


@attr.s(auto_attribs=True)
class PispgatewayAspsProviderResponse:
    """
    Attributes:
        capabilities (Union[Unset, List['PispgatewayCapability']]): Capability list of the ASPSP
        id (Union[Unset, str]): Unique identifier (within Modulr) of the ASPSP Example: H100000001.
        name (Union[Unset, str]): Name of the ASPSP Example: Bank of Money.
    """

    capabilities: Union[Unset, List["PispgatewayCapability"]] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        capabilities: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = []
            for capabilities_item_data in self.capabilities:
                capabilities_item = capabilities_item_data.to_dict()

                capabilities.append(capabilities_item)

        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pispgateway_capability import PispgatewayCapability

        d = src_dict.copy()
        capabilities = []
        _capabilities = d.pop("capabilities", UNSET)
        for capabilities_item_data in _capabilities or []:
            capabilities_item = PispgatewayCapability.from_dict(capabilities_item_data)

            capabilities.append(capabilities_item)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        pispgateway_asps_provider_response = cls(
            capabilities=capabilities,
            id=id,
            name=name,
        )

        pispgateway_asps_provider_response.additional_properties = d
        return pispgateway_asps_provider_response

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
