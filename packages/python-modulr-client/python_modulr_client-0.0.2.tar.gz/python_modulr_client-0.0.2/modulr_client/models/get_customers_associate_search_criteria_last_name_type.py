from enum import Enum


class GetCustomersAssociateSearchCriteriaLastNameType(str, Enum):
    WORD_MATCH = "WORD_MATCH"
    CONTAINS = "CONTAINS"
    EXACT = "EXACT"
    SUFFIX = "SUFFIX"
    PREFIX = "PREFIX"
    WORD_MATCH_ALPHANUMERIC = "WORD_MATCH_ALPHANUMERIC"

    def __str__(self) -> str:
        return str(self.value)
