import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.card_card_response_format import CardCardResponseFormat
from ..models.card_card_response_status import CardCardResponseStatus
from ..models.card_card_response_three_d_secure_status import (
    CardCardResponseThreeDSecureStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_card_constraints import CardCardConstraints
    from ..models.card_card_holder import CardCardHolder
    from ..models.card_card_three_d_secure_authentication import (
        CardCardThreeDSecureAuthentication,
    )
    from ..models.card_product_design_detail import CardProductDesignDetail


T = TypeVar("T", bound="CardCardResponse")


@attr.s(auto_attribs=True)
class CardCardResponse:
    """
    Attributes:
        account_bid (Union[Unset, str]): Account identifier Example: A020N8PD.
        authentication (Union[Unset, CardCardThreeDSecureAuthentication]): The 3DS authentication method statuses
        card_scheme (Union[Unset, str]): Card scheme. MASTERCARD or VISA Example: MASTERCARD.
        card_type (Union[Unset, str]): Card product type Example: Business.
        constraints (Union[Unset, CardCardConstraints]): CardConstraints
        created_date (Union[Unset, datetime.datetime]):
        currency (Union[Unset, str]): A 3 letter ISO 4217 code representing the card currency Example: GBP.
        design (Union[Unset, CardProductDesignDetail]): Design references for physical card and packaging
        expiry (Union[Unset, str]): An ISO 8601 date with year & month components only Example: 2018-12.
        external_ref (Union[Unset, str]): Client reference for the newly created card. Maximum of 50 characters.
            Example: TTQ_51211.
        format_ (Union[Unset, CardCardResponseFormat]): The format of the card.  PHYSICAL or VIRTUAL Example: PHYSICAL.
        holder (Union[Unset, CardCardHolder]): CardHolder
        id (Union[Unset, str]): Card identifier. Maximum of 10 alphanumeric characters Example: V000000001.
        limit (Union[Unset, str]): Total card authorisation limit Example: 1000.0.
        masked_pan (Union[Unset, str]): Masked card PAN Example: 527095******3544.
        max_limit (Union[Unset, str]): Maximum limit which can be set on this card and is the maximum lifetime spend the
            card can have Example: 4000.0.
        printed_name (Union[Unset, str]): Name printed on the card. Will only be returned for physical cards. Maximum of
            20 alphanumeric characters (including full stop, hyphen, apostrophe, caret and space)
        spend (Union[Unset, str]): Current total of all authorisations on this card Example: 250.0.
        status (Union[Unset, CardCardResponseStatus]): The current state of the card.
        three_d_secure_status (Union[Unset, CardCardResponseThreeDSecureStatus]): The 3DS status of the card, based on
            the SMS one time password Example: ENROLLED.
    """

    account_bid: Union[Unset, str] = UNSET
    authentication: Union[Unset, "CardCardThreeDSecureAuthentication"] = UNSET
    card_scheme: Union[Unset, str] = UNSET
    card_type: Union[Unset, str] = UNSET
    constraints: Union[Unset, "CardCardConstraints"] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    currency: Union[Unset, str] = UNSET
    design: Union[Unset, "CardProductDesignDetail"] = UNSET
    expiry: Union[Unset, str] = UNSET
    external_ref: Union[Unset, str] = UNSET
    format_: Union[Unset, CardCardResponseFormat] = UNSET
    holder: Union[Unset, "CardCardHolder"] = UNSET
    id: Union[Unset, str] = UNSET
    limit: Union[Unset, str] = UNSET
    masked_pan: Union[Unset, str] = UNSET
    max_limit: Union[Unset, str] = UNSET
    printed_name: Union[Unset, str] = UNSET
    spend: Union[Unset, str] = UNSET
    status: Union[Unset, CardCardResponseStatus] = UNSET
    three_d_secure_status: Union[Unset, CardCardResponseThreeDSecureStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_bid = self.account_bid
        authentication: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.authentication, Unset):
            authentication = self.authentication.to_dict()

        card_scheme = self.card_scheme
        card_type = self.card_type
        constraints: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constraints, Unset):
            constraints = self.constraints.to_dict()

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        currency = self.currency
        design: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.design, Unset):
            design = self.design.to_dict()

        expiry = self.expiry
        external_ref = self.external_ref
        format_: Union[Unset, str] = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

        holder: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.holder, Unset):
            holder = self.holder.to_dict()

        id = self.id
        limit = self.limit
        masked_pan = self.masked_pan
        max_limit = self.max_limit
        printed_name = self.printed_name
        spend = self.spend
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        three_d_secure_status: Union[Unset, str] = UNSET
        if not isinstance(self.three_d_secure_status, Unset):
            three_d_secure_status = self.three_d_secure_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_bid is not UNSET:
            field_dict["accountBid"] = account_bid
        if authentication is not UNSET:
            field_dict["authentication"] = authentication
        if card_scheme is not UNSET:
            field_dict["cardScheme"] = card_scheme
        if card_type is not UNSET:
            field_dict["cardType"] = card_type
        if constraints is not UNSET:
            field_dict["constraints"] = constraints
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if currency is not UNSET:
            field_dict["currency"] = currency
        if design is not UNSET:
            field_dict["design"] = design
        if expiry is not UNSET:
            field_dict["expiry"] = expiry
        if external_ref is not UNSET:
            field_dict["externalRef"] = external_ref
        if format_ is not UNSET:
            field_dict["format"] = format_
        if holder is not UNSET:
            field_dict["holder"] = holder
        if id is not UNSET:
            field_dict["id"] = id
        if limit is not UNSET:
            field_dict["limit"] = limit
        if masked_pan is not UNSET:
            field_dict["maskedPan"] = masked_pan
        if max_limit is not UNSET:
            field_dict["maxLimit"] = max_limit
        if printed_name is not UNSET:
            field_dict["printedName"] = printed_name
        if spend is not UNSET:
            field_dict["spend"] = spend
        if status is not UNSET:
            field_dict["status"] = status
        if three_d_secure_status is not UNSET:
            field_dict["threeDSecureStatus"] = three_d_secure_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_card_constraints import CardCardConstraints
        from ..models.card_card_holder import CardCardHolder
        from ..models.card_card_three_d_secure_authentication import (
            CardCardThreeDSecureAuthentication,
        )
        from ..models.card_product_design_detail import CardProductDesignDetail

        d = src_dict.copy()
        account_bid = d.pop("accountBid", UNSET)

        _authentication = d.pop("authentication", UNSET)
        authentication: Union[Unset, CardCardThreeDSecureAuthentication]
        if isinstance(_authentication, Unset):
            authentication = UNSET
        else:
            authentication = CardCardThreeDSecureAuthentication.from_dict(_authentication)

        card_scheme = d.pop("cardScheme", UNSET)

        card_type = d.pop("cardType", UNSET)

        _constraints = d.pop("constraints", UNSET)
        constraints: Union[Unset, CardCardConstraints]
        if isinstance(_constraints, Unset):
            constraints = UNSET
        else:
            constraints = CardCardConstraints.from_dict(_constraints)

        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date, Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)

        currency = d.pop("currency", UNSET)

        _design = d.pop("design", UNSET)
        design: Union[Unset, CardProductDesignDetail]
        if isinstance(_design, Unset):
            design = UNSET
        else:
            design = CardProductDesignDetail.from_dict(_design)

        expiry = d.pop("expiry", UNSET)

        external_ref = d.pop("externalRef", UNSET)

        _format_ = d.pop("format", UNSET)
        format_: Union[Unset, CardCardResponseFormat]
        if isinstance(_format_, Unset):
            format_ = UNSET
        else:
            format_ = CardCardResponseFormat(_format_)

        _holder = d.pop("holder", UNSET)
        holder: Union[Unset, CardCardHolder]
        if isinstance(_holder, Unset):
            holder = UNSET
        else:
            holder = CardCardHolder.from_dict(_holder)

        id = d.pop("id", UNSET)

        limit = d.pop("limit", UNSET)

        masked_pan = d.pop("maskedPan", UNSET)

        max_limit = d.pop("maxLimit", UNSET)

        printed_name = d.pop("printedName", UNSET)

        spend = d.pop("spend", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CardCardResponseStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CardCardResponseStatus(_status)

        _three_d_secure_status = d.pop("threeDSecureStatus", UNSET)
        three_d_secure_status: Union[Unset, CardCardResponseThreeDSecureStatus]
        if isinstance(_three_d_secure_status, Unset):
            three_d_secure_status = UNSET
        else:
            three_d_secure_status = CardCardResponseThreeDSecureStatus(_three_d_secure_status)

        card_card_response = cls(
            account_bid=account_bid,
            authentication=authentication,
            card_scheme=card_scheme,
            card_type=card_type,
            constraints=constraints,
            created_date=created_date,
            currency=currency,
            design=design,
            expiry=expiry,
            external_ref=external_ref,
            format_=format_,
            holder=holder,
            id=id,
            limit=limit,
            masked_pan=masked_pan,
            max_limit=max_limit,
            printed_name=printed_name,
            spend=spend,
            status=status,
            three_d_secure_status=three_d_secure_status,
        )

        card_card_response.additional_properties = d
        return card_card_response

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
