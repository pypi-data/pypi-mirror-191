from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.rule_rule_config_data_days_to_run_item import (
    RuleRuleConfigDataDaysToRunItem,
)
from ..models.rule_rule_config_data_frequency import RuleRuleConfigDataFrequency
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rule_conditional_split_config import RuleConditionalSplitConfig
    from ..models.rule_split_config import RuleSplitConfig


T = TypeVar("T", bound="RuleRuleConfigData")


@attr.s(auto_attribs=True)
class RuleRuleConfigData:
    """Configuration fields for all types of rules. To be populated where applicable based on rule type.

    Attributes:
        balance_to_leave (Union[Unset, float]): Balance to be left after the rule has been ran. e.g. 100.00. Sweep Rule
            Only
        conditional_split_config (Union[Unset, RuleConditionalSplitConfig]): Configuration for a Conditional Split Rule
        conditional_splits (Union[Unset, List['RuleSplitConfig']]):
        days_to_run (Union[Unset, List[RuleRuleConfigDataDaysToRunItem]]): Day(s) of the week the rule is to run. e.g.
            ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]. Sweep Rule Only
        destination_id (Union[Unset, str]): Id of destination beneficiary. e.g. B1000001. Sweep Rule Only
        frequency (Union[Unset, RuleRuleConfigDataFrequency]): Frequency of the rule. Sweep Rule Only
        source_id (Union[Unset, str]): Account to fund the supplied accountId. e.g. A1000002. Funding Rule Only
        splits (Union[Unset, List['RuleSplitConfig']]):
        trigger_balance (Union[Unset, float]): Minimum balance required to trigger the rule. e.g. 100.00. Sweep Rule
            Only
    """

    balance_to_leave: Union[Unset, float] = UNSET
    conditional_split_config: Union[Unset, "RuleConditionalSplitConfig"] = UNSET
    conditional_splits: Union[Unset, List["RuleSplitConfig"]] = UNSET
    days_to_run: Union[Unset, List[RuleRuleConfigDataDaysToRunItem]] = UNSET
    destination_id: Union[Unset, str] = UNSET
    frequency: Union[Unset, RuleRuleConfigDataFrequency] = UNSET
    source_id: Union[Unset, str] = UNSET
    splits: Union[Unset, List["RuleSplitConfig"]] = UNSET
    trigger_balance: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        balance_to_leave = self.balance_to_leave
        conditional_split_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.conditional_split_config, Unset):
            conditional_split_config = self.conditional_split_config.to_dict()

        conditional_splits: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conditional_splits, Unset):
            conditional_splits = []
            for conditional_splits_item_data in self.conditional_splits:
                conditional_splits_item = conditional_splits_item_data.to_dict()

                conditional_splits.append(conditional_splits_item)

        days_to_run: Union[Unset, List[str]] = UNSET
        if not isinstance(self.days_to_run, Unset):
            days_to_run = []
            for days_to_run_item_data in self.days_to_run:
                days_to_run_item = days_to_run_item_data.value

                days_to_run.append(days_to_run_item)

        destination_id = self.destination_id
        frequency: Union[Unset, str] = UNSET
        if not isinstance(self.frequency, Unset):
            frequency = self.frequency.value

        source_id = self.source_id
        splits: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.splits, Unset):
            splits = []
            for splits_item_data in self.splits:
                splits_item = splits_item_data.to_dict()

                splits.append(splits_item)

        trigger_balance = self.trigger_balance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balance_to_leave is not UNSET:
            field_dict["balanceToLeave"] = balance_to_leave
        if conditional_split_config is not UNSET:
            field_dict["conditionalSplitConfig"] = conditional_split_config
        if conditional_splits is not UNSET:
            field_dict["conditionalSplits"] = conditional_splits
        if days_to_run is not UNSET:
            field_dict["daysToRun"] = days_to_run
        if destination_id is not UNSET:
            field_dict["destinationId"] = destination_id
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if source_id is not UNSET:
            field_dict["sourceId"] = source_id
        if splits is not UNSET:
            field_dict["splits"] = splits
        if trigger_balance is not UNSET:
            field_dict["triggerBalance"] = trigger_balance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.rule_conditional_split_config import RuleConditionalSplitConfig
        from ..models.rule_split_config import RuleSplitConfig

        d = src_dict.copy()
        balance_to_leave = d.pop("balanceToLeave", UNSET)

        _conditional_split_config = d.pop("conditionalSplitConfig", UNSET)
        conditional_split_config: Union[Unset, RuleConditionalSplitConfig]
        if isinstance(_conditional_split_config, Unset):
            conditional_split_config = UNSET
        else:
            conditional_split_config = RuleConditionalSplitConfig.from_dict(
                _conditional_split_config
            )

        conditional_splits = []
        _conditional_splits = d.pop("conditionalSplits", UNSET)
        for conditional_splits_item_data in _conditional_splits or []:
            conditional_splits_item = RuleSplitConfig.from_dict(conditional_splits_item_data)

            conditional_splits.append(conditional_splits_item)

        days_to_run = []
        _days_to_run = d.pop("daysToRun", UNSET)
        for days_to_run_item_data in _days_to_run or []:
            days_to_run_item = RuleRuleConfigDataDaysToRunItem(days_to_run_item_data)

            days_to_run.append(days_to_run_item)

        destination_id = d.pop("destinationId", UNSET)

        _frequency = d.pop("frequency", UNSET)
        frequency: Union[Unset, RuleRuleConfigDataFrequency]
        if isinstance(_frequency, Unset):
            frequency = UNSET
        else:
            frequency = RuleRuleConfigDataFrequency(_frequency)

        source_id = d.pop("sourceId", UNSET)

        splits = []
        _splits = d.pop("splits", UNSET)
        for splits_item_data in _splits or []:
            splits_item = RuleSplitConfig.from_dict(splits_item_data)

            splits.append(splits_item)

        trigger_balance = d.pop("triggerBalance", UNSET)

        rule_rule_config_data = cls(
            balance_to_leave=balance_to_leave,
            conditional_split_config=conditional_split_config,
            conditional_splits=conditional_splits,
            days_to_run=days_to_run,
            destination_id=destination_id,
            frequency=frequency,
            source_id=source_id,
            splits=splits,
            trigger_balance=trigger_balance,
        )

        rule_rule_config_data.additional_properties = d
        return rule_rule_config_data

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
