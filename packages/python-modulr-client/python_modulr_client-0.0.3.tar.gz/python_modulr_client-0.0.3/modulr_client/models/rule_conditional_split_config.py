from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RuleConditionalSplitConfig")


@attr.s(auto_attribs=True)
class RuleConditionalSplitConfig:
    """Configuration for a Conditional Split Rule

    Attributes:
        condition_amount (float): Amount the conditional split rule should reach before defaulting to the split rule.
            e.g. 100.
        destination_id (str): Id of destination beneficiary. e.g. B1000001.
        percent (str): Percentage of payment to be moved to specified destination. e.g. 7.25.
        condition_done (Union[Unset, bool]): Whether the condition amount has been met. e.g. true or false
    """

    condition_amount: float
    destination_id: str
    percent: str
    condition_done: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        condition_amount = self.condition_amount
        destination_id = self.destination_id
        percent = self.percent
        condition_done = self.condition_done

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conditionAmount": condition_amount,
                "destinationId": destination_id,
                "percent": percent,
            }
        )
        if condition_done is not UNSET:
            field_dict["conditionDone"] = condition_done

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        condition_amount = d.pop("conditionAmount")

        destination_id = d.pop("destinationId")

        percent = d.pop("percent")

        condition_done = d.pop("conditionDone", UNSET)

        rule_conditional_split_config = cls(
            condition_amount=condition_amount,
            destination_id=destination_id,
            percent=percent,
            condition_done=condition_done,
        )

        rule_conditional_split_config.additional_properties = d
        return rule_conditional_split_config

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
