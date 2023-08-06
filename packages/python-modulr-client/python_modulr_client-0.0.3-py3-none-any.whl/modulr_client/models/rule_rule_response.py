from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.rule_rule_response_type import RuleRuleResponseType

if TYPE_CHECKING:
    from ..models.rule_rule_config_data import RuleRuleConfigData


T = TypeVar("T", bound="RuleRuleResponse")


@attr.s(auto_attribs=True)
class RuleRuleResponse:
    """
    Attributes:
        account_id (str): The Account which the Rule is created on. Example: A1000001.
        data (RuleRuleConfigData): Configuration fields for all types of rules. To be populated where applicable based
            on rule type.
        id (str): Unique identifier for a Rule Example: R1000001.
        name (str): Rule's name Example: My new rule.
        type (RuleRuleResponseType): The type of Rule. Can be one of the following {SWEEP, SPLIT, FUNDING}
    """

    account_id: str
    data: "RuleRuleConfigData"
    id: str
    name: str
    type: RuleRuleResponseType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        data = self.data.to_dict()

        id = self.id
        name = self.name
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "data": data,
                "id": id,
                "name": name,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.rule_rule_config_data import RuleRuleConfigData

        d = src_dict.copy()
        account_id = d.pop("accountId")

        data = RuleRuleConfigData.from_dict(d.pop("data"))

        id = d.pop("id")

        name = d.pop("name")

        type = RuleRuleResponseType(d.pop("type"))

        rule_rule_response = cls(
            account_id=account_id,
            data=data,
            id=id,
            name=name,
            type=type,
        )

        rule_rule_response.additional_properties = d
        return rule_rule_response

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
