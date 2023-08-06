from enum import Enum


class RuleRuleResponseType(str, Enum):
    FUNDING = "FUNDING"
    SPLIT = "SPLIT"
    SWEEP = "SWEEP"

    def __str__(self) -> str:
        return str(self.value)
