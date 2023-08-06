from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_authorisation_constraints import CardAuthorisationConstraints


T = TypeVar("T", bound="CardCardConstraints")


@attr.s(auto_attribs=True)
class CardCardConstraints:
    """CardConstraints

    Attributes:
        mcc_whitelist (List[str]): mccWhitelist Example: ['1000', '1002-3000', '5060'].
        authorisation (Union[Unset, CardAuthorisationConstraints]): Authorisation constraints
    """

    mcc_whitelist: List[str]
    authorisation: Union[Unset, "CardAuthorisationConstraints"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mcc_whitelist = self.mcc_whitelist

        authorisation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.authorisation, Unset):
            authorisation = self.authorisation.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mccWhitelist": mcc_whitelist,
            }
        )
        if authorisation is not UNSET:
            field_dict["authorisation"] = authorisation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_authorisation_constraints import CardAuthorisationConstraints

        d = src_dict.copy()
        mcc_whitelist = cast(List[str], d.pop("mccWhitelist"))

        _authorisation = d.pop("authorisation", UNSET)
        authorisation: Union[Unset, CardAuthorisationConstraints]
        if isinstance(_authorisation, Unset):
            authorisation = UNSET
        else:
            authorisation = CardAuthorisationConstraints.from_dict(_authorisation)

        card_card_constraints = cls(
            mcc_whitelist=mcc_whitelist,
            authorisation=authorisation,
        )

        card_card_constraints.additional_properties = d
        return card_card_constraints

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
