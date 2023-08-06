from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentOverseasAccountIdentifier")


@attr.s(auto_attribs=True)
class PaymentOverseasAccountIdentifier:
    """
    Attributes:
        bban (Union[Unset, str]): Basic Bank Account Number (BBAN) Example: NWBK60161331926819.
        iban (Union[Unset, str]): International Bank Account Number (IBAN) Example: GB20MODR00000000000001.
        other_account_number (Union[Unset, str]): Other Account ID Example: 987654321.
        upic (Union[Unset, str]): Universal Payment Identification Code (UPIC) Example: 987654321.
    """

    bban: Union[Unset, str] = UNSET
    iban: Union[Unset, str] = UNSET
    other_account_number: Union[Unset, str] = UNSET
    upic: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bban = self.bban
        iban = self.iban
        other_account_number = self.other_account_number
        upic = self.upic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bban is not UNSET:
            field_dict["bban"] = bban
        if iban is not UNSET:
            field_dict["iban"] = iban
        if other_account_number is not UNSET:
            field_dict["otherAccountNumber"] = other_account_number
        if upic is not UNSET:
            field_dict["upic"] = upic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bban = d.pop("bban", UNSET)

        iban = d.pop("iban", UNSET)

        other_account_number = d.pop("otherAccountNumber", UNSET)

        upic = d.pop("upic", UNSET)

        payment_overseas_account_identifier = cls(
            bban=bban,
            iban=iban,
            other_account_number=other_account_number,
            upic=upic,
        )

        payment_overseas_account_identifier.additional_properties = d
        return payment_overseas_account_identifier

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
