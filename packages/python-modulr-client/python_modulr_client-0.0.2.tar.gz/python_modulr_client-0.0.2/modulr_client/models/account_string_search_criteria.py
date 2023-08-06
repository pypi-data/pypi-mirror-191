from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.account_string_search_criteria_type import AccountStringSearchCriteriaType

T = TypeVar("T", bound="AccountStringSearchCriteria")


@attr.s(auto_attribs=True)
class AccountStringSearchCriteria:
    """
    Attributes:
        type (AccountStringSearchCriteriaType): WORD_MATCH - using word boundaries,
            WORD_MATCH_ALPHANUMERIC - using word boundaries, but replaces non-alphanumeric characters in the search with a
            word boundary match,
            PREFIX - same case prefix,
            SUFFIX - same case suffix,
            CONTAINS - same case contains
            EXACT - same case exact
        value (str):
    """

    type: AccountStringSearchCriteriaType
    value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = AccountStringSearchCriteriaType(d.pop("type"))

        value = d.pop("value")

        account_string_search_criteria = cls(
            type=type,
            value=value,
        )

        account_string_search_criteria.additional_properties = d
        return account_string_search_criteria

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
