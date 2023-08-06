from enum import Enum


class RuleRuleConfigDataFrequency(str, Enum):
    Daily = "Daily"

    def __str__(self) -> str:
        return str(self.value)
