from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RuleSplitConfig")


@attr.s(auto_attribs=True)
class RuleSplitConfig:
    """Configuration for a Split Rule

    Attributes:
        destination_id (str): Id of destination beneficiary. e.g. B1000001.
        percent (str): Percentage of payment to be moved to specified destination. e.g. 7.25.
    """

    destination_id: str
    percent: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        destination_id = self.destination_id
        percent = self.percent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destinationId": destination_id,
                "percent": percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        destination_id = d.pop("destinationId")

        percent = d.pop("percent")

        rule_split_config = cls(
            destination_id=destination_id,
            percent=percent,
        )

        rule_split_config.additional_properties = d
        return rule_split_config

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
