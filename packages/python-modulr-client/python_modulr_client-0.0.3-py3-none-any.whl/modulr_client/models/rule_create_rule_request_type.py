from enum import Enum


class RuleCreateRuleRequestType(str, Enum):
    FUNDING = "FUNDING"
    SPLIT = "SPLIT"
    SWEEP = "SWEEP"

    def __str__(self) -> str:
        return str(self.value)
