from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.cardsimulator_card_authorisation_response_billing_currency import (
    CardsimulatorCardAuthorisationResponseBillingCurrency,
)
from ..models.cardsimulator_card_authorisation_response_status import (
    CardsimulatorCardAuthorisationResponseStatus,
)
from ..models.cardsimulator_card_authorisation_response_transaction_currency import (
    CardsimulatorCardAuthorisationResponseTransactionCurrency,
)

T = TypeVar("T", bound="CardsimulatorCardAuthorisationResponse")


@attr.s(auto_attribs=True)
class CardsimulatorCardAuthorisationResponse:
    """CardAuthorisationResponse

    Attributes:
        authorisation_id (str): Authorisation Id Example: A00000000X.
        billing_amount (float): Authorisation billing amount Example: 80.
        billing_currency (CardsimulatorCardAuthorisationResponseBillingCurrency): Currency of the card Example: GBP.
        card_id (str): Card Id Example: V000000001.
        fx_rate (float): Foreign exchange rate used between transaction and billing currencies Example: 0.8.
        mcc (str): Merchant Category Code Example: 5812.
        status (CardsimulatorCardAuthorisationResponseStatus): Authorisation Status [APPROVED, REVERSED, SETTLED]
            Example: APPROVED.
        transaction_amount (float): Authorisation Transaction Amount Example: 100.
        transaction_currency (CardsimulatorCardAuthorisationResponseTransactionCurrency): Currency for this transaction
            Example: EUR.
    """

    authorisation_id: str
    billing_amount: float
    billing_currency: CardsimulatorCardAuthorisationResponseBillingCurrency
    card_id: str
    fx_rate: float
    mcc: str
    status: CardsimulatorCardAuthorisationResponseStatus
    transaction_amount: float
    transaction_currency: CardsimulatorCardAuthorisationResponseTransactionCurrency
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        authorisation_id = self.authorisation_id
        billing_amount = self.billing_amount
        billing_currency = self.billing_currency.value

        card_id = self.card_id
        fx_rate = self.fx_rate
        mcc = self.mcc
        status = self.status.value

        transaction_amount = self.transaction_amount
        transaction_currency = self.transaction_currency.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "authorisationId": authorisation_id,
                "billingAmount": billing_amount,
                "billingCurrency": billing_currency,
                "cardId": card_id,
                "fxRate": fx_rate,
                "mcc": mcc,
                "status": status,
                "transactionAmount": transaction_amount,
                "transactionCurrency": transaction_currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        authorisation_id = d.pop("authorisationId")

        billing_amount = d.pop("billingAmount")

        billing_currency = CardsimulatorCardAuthorisationResponseBillingCurrency(
            d.pop("billingCurrency")
        )

        card_id = d.pop("cardId")

        fx_rate = d.pop("fxRate")

        mcc = d.pop("mcc")

        status = CardsimulatorCardAuthorisationResponseStatus(d.pop("status"))

        transaction_amount = d.pop("transactionAmount")

        transaction_currency = CardsimulatorCardAuthorisationResponseTransactionCurrency(
            d.pop("transactionCurrency")
        )

        cardsimulator_card_authorisation_response = cls(
            authorisation_id=authorisation_id,
            billing_amount=billing_amount,
            billing_currency=billing_currency,
            card_id=card_id,
            fx_rate=fx_rate,
            mcc=mcc,
            status=status,
            transaction_amount=transaction_amount,
            transaction_currency=transaction_currency,
        )

        cardsimulator_card_authorisation_response.additional_properties = d
        return cardsimulator_card_authorisation_response

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
