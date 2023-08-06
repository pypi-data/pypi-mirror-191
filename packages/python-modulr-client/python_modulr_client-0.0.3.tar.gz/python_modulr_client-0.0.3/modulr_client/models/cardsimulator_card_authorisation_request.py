from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cardsimulator_card_authorisation_request_transaction_currency import (
    CardsimulatorCardAuthorisationRequestTransactionCurrency,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardsimulatorCardAuthorisationRequest")


@attr.s(auto_attribs=True)
class CardsimulatorCardAuthorisationRequest:
    """Details of the authorisation to create

    Attributes:
        mcc (str): Merchant Category Code Example: 5812.
        transaction_amount (float): The transaction amount Example: 5.45.
        fx_rate (Union[Unset, float]): The foreign exchange rate to use, when transaction currency differs from billing
            currency. Defaults to 1.0 Example: 0.8.
        transaction_currency (Union[Unset, CardsimulatorCardAuthorisationRequestTransactionCurrency]): The transaction
            currency. Defaults to the card's billing currency Example: GBP.
    """

    mcc: str
    transaction_amount: float
    fx_rate: Union[Unset, float] = UNSET
    transaction_currency: Union[
        Unset, CardsimulatorCardAuthorisationRequestTransactionCurrency
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mcc = self.mcc
        transaction_amount = self.transaction_amount
        fx_rate = self.fx_rate
        transaction_currency: Union[Unset, str] = UNSET
        if not isinstance(self.transaction_currency, Unset):
            transaction_currency = self.transaction_currency.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mcc": mcc,
                "transactionAmount": transaction_amount,
            }
        )
        if fx_rate is not UNSET:
            field_dict["fxRate"] = fx_rate
        if transaction_currency is not UNSET:
            field_dict["transactionCurrency"] = transaction_currency

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mcc = d.pop("mcc")

        transaction_amount = d.pop("transactionAmount")

        fx_rate = d.pop("fxRate", UNSET)

        _transaction_currency = d.pop("transactionCurrency", UNSET)
        transaction_currency: Union[
            Unset, CardsimulatorCardAuthorisationRequestTransactionCurrency
        ]
        if isinstance(_transaction_currency, Unset):
            transaction_currency = UNSET
        else:
            transaction_currency = CardsimulatorCardAuthorisationRequestTransactionCurrency(
                _transaction_currency
            )

        cardsimulator_card_authorisation_request = cls(
            mcc=mcc,
            transaction_amount=transaction_amount,
            fx_rate=fx_rate,
            transaction_currency=transaction_currency,
        )

        cardsimulator_card_authorisation_request.additional_properties = d
        return cardsimulator_card_authorisation_request

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
