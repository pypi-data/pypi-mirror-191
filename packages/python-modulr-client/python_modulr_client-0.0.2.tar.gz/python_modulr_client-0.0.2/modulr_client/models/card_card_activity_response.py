import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.card_card_activity_response_status import CardCardActivityResponseStatus
from ..models.card_card_activity_response_type import CardCardActivityResponseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_auth_info import CardAuthInfo


T = TypeVar("T", bound="CardCardActivityResponse")


@attr.s(auto_attribs=True)
class CardCardActivityResponse:
    """List of responses on the current page

    Attributes:
        billing_amount (float): The card activity billing amount Example: 678.91.
        billing_currency (str): The 3 letter ISO 4217 card activity billing currency Example: GBP.
        card_id (str): Card identifier. Maximum of 10 alphanumeric characters Example: V000000001.
        created_date (datetime.datetime): The creation date of the card activity
        fx_rate (float): The FX rate applied to any conversion between transaction & billing amount. Rounded to 6
            decimal places and zero padded Example: 1.123456.
        id (str): The card activity identifier. Maximum of 10 alphanumeric characters Example: X000000001.
        mcc (str): The Merchant Category Code (MCC) for the card activity. Follows ISO-18245 format Example: 5182.
        order_id (str): Order identifier which links together related authorisations, reversals & settlements. Maximum
            of 10 alphanumeric characters Example: 1234.
        transaction_amount (float): The card activity transaction amount Example: 123.45.
        transaction_currency (str): The 3 letter ISO 4217 card activity transaction currency Example: EUR.
        type (CardCardActivityResponseType): Type of card activity
        authorisation_info (Union[Unset, CardAuthInfo]): Authorisation information of the activity
        card_token_device_id (Union[Unset, str]): The bound card token device associated with this activity, if a
            tokenised card was used.
        card_token_id (Union[Unset, str]): The card token associated with this activity, if a tokenised card was used.
        merchant_country (Union[Unset, str]): The 3 letter ISO 3166 merchant country code Example: GBR.
        merchant_name (Union[Unset, str]): The merchant name Example: Loudons Cafe.
        reason (Union[Unset, str]): The reason why this activity was declined. Only applies to activities with status
            DECLINED Example: Account has insufficient funds.
        status (Union[Unset, CardCardActivityResponseStatus]): Status of card activity. Only applies to activities of
            type AUTHORISATION
        verified_by_3ds (Union[Unset, bool]): Whether the activity was 3DS enabled
    """

    billing_amount: float
    billing_currency: str
    card_id: str
    created_date: datetime.datetime
    fx_rate: float
    id: str
    mcc: str
    order_id: str
    transaction_amount: float
    transaction_currency: str
    type: CardCardActivityResponseType
    authorisation_info: Union[Unset, "CardAuthInfo"] = UNSET
    card_token_device_id: Union[Unset, str] = UNSET
    card_token_id: Union[Unset, str] = UNSET
    merchant_country: Union[Unset, str] = UNSET
    merchant_name: Union[Unset, str] = UNSET
    reason: Union[Unset, str] = UNSET
    status: Union[Unset, CardCardActivityResponseStatus] = UNSET
    verified_by_3ds: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        billing_amount = self.billing_amount
        billing_currency = self.billing_currency
        card_id = self.card_id
        created_date = self.created_date.isoformat()

        fx_rate = self.fx_rate
        id = self.id
        mcc = self.mcc
        order_id = self.order_id
        transaction_amount = self.transaction_amount
        transaction_currency = self.transaction_currency
        type = self.type.value

        authorisation_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.authorisation_info, Unset):
            authorisation_info = self.authorisation_info.to_dict()

        card_token_device_id = self.card_token_device_id
        card_token_id = self.card_token_id
        merchant_country = self.merchant_country
        merchant_name = self.merchant_name
        reason = self.reason
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        verified_by_3ds = self.verified_by_3ds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "billingAmount": billing_amount,
                "billingCurrency": billing_currency,
                "cardId": card_id,
                "createdDate": created_date,
                "fxRate": fx_rate,
                "id": id,
                "mcc": mcc,
                "orderId": order_id,
                "transactionAmount": transaction_amount,
                "transactionCurrency": transaction_currency,
                "type": type,
            }
        )
        if authorisation_info is not UNSET:
            field_dict["authorisationInfo"] = authorisation_info
        if card_token_device_id is not UNSET:
            field_dict["cardTokenDeviceId"] = card_token_device_id
        if card_token_id is not UNSET:
            field_dict["cardTokenId"] = card_token_id
        if merchant_country is not UNSET:
            field_dict["merchantCountry"] = merchant_country
        if merchant_name is not UNSET:
            field_dict["merchantName"] = merchant_name
        if reason is not UNSET:
            field_dict["reason"] = reason
        if status is not UNSET:
            field_dict["status"] = status
        if verified_by_3ds is not UNSET:
            field_dict["verifiedBy3DS"] = verified_by_3ds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_auth_info import CardAuthInfo

        d = src_dict.copy()
        billing_amount = d.pop("billingAmount")

        billing_currency = d.pop("billingCurrency")

        card_id = d.pop("cardId")

        created_date = isoparse(d.pop("createdDate"))

        fx_rate = d.pop("fxRate")

        id = d.pop("id")

        mcc = d.pop("mcc")

        order_id = d.pop("orderId")

        transaction_amount = d.pop("transactionAmount")

        transaction_currency = d.pop("transactionCurrency")

        type = CardCardActivityResponseType(d.pop("type"))

        _authorisation_info = d.pop("authorisationInfo", UNSET)
        authorisation_info: Union[Unset, CardAuthInfo]
        if isinstance(_authorisation_info, Unset):
            authorisation_info = UNSET
        else:
            authorisation_info = CardAuthInfo.from_dict(_authorisation_info)

        card_token_device_id = d.pop("cardTokenDeviceId", UNSET)

        card_token_id = d.pop("cardTokenId", UNSET)

        merchant_country = d.pop("merchantCountry", UNSET)

        merchant_name = d.pop("merchantName", UNSET)

        reason = d.pop("reason", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CardCardActivityResponseStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CardCardActivityResponseStatus(_status)

        verified_by_3ds = d.pop("verifiedBy3DS", UNSET)

        card_card_activity_response = cls(
            billing_amount=billing_amount,
            billing_currency=billing_currency,
            card_id=card_id,
            created_date=created_date,
            fx_rate=fx_rate,
            id=id,
            mcc=mcc,
            order_id=order_id,
            transaction_amount=transaction_amount,
            transaction_currency=transaction_currency,
            type=type,
            authorisation_info=authorisation_info,
            card_token_device_id=card_token_device_id,
            card_token_id=card_token_id,
            merchant_country=merchant_country,
            merchant_name=merchant_name,
            reason=reason,
            status=status,
            verified_by_3ds=verified_by_3ds,
        )

        card_card_activity_response.additional_properties = d
        return card_card_activity_response

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
