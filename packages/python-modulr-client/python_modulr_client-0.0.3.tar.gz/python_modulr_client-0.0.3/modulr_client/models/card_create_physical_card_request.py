from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.card_address_detail import CardAddressDetail
    from ..models.card_card_authentication import CardCardAuthentication
    from ..models.card_card_holder import CardCardHolder
    from ..models.card_constraints import CardConstraints
    from ..models.card_product_design_detail import CardProductDesignDetail


T = TypeVar("T", bound="CardCreatePhysicalCardRequest")


@attr.s(auto_attribs=True)
class CardCreatePhysicalCardRequest:
    """Card

    Attributes:
        design (CardProductDesignDetail): Design references for physical card and packaging
        expiry (str): ISO 8601 date with year & month components only. The supplied value must be in the future (cannot
            be the current month) and is _inclusive_ of the specified month. Example: 2018-12.
        external_ref (str): Client reference for the newly created card. Maximum of 50 alphanumeric characters
            (including underscore, hyphen and space).
        holder (CardCardHolder): CardHolder
        limit (float): Total card authorisation limit. Example: 1000.
        printed_name (str): Name to be printed on the card. Maximum of 20 alphanumeric characters (including full stop,
            hyphen, apostrophe, caret and space) Example: Joe Bloggs.
        product_code (str): Identifies the _type_ of card to create (GBP consumer, GBP business, etc). Modulr will
            supply a list of possible values.
        authentication (Union[Unset, CardCardAuthentication]): Authentication
        constraints (Union[Unset, CardConstraints]): Constraints
        shipping_address (Union[Unset, CardAddressDetail]): Address details for the cardholder. Optional for individual
            customers whose partner has verification type EXTERNAL.
    """

    design: "CardProductDesignDetail"
    expiry: str
    external_ref: str
    holder: "CardCardHolder"
    limit: float
    printed_name: str
    product_code: str
    authentication: Union[Unset, "CardCardAuthentication"] = UNSET
    constraints: Union[Unset, "CardConstraints"] = UNSET
    shipping_address: Union[Unset, "CardAddressDetail"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        design = self.design.to_dict()

        expiry = self.expiry
        external_ref = self.external_ref
        holder = self.holder.to_dict()

        limit = self.limit
        printed_name = self.printed_name
        product_code = self.product_code
        authentication: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.authentication, Unset):
            authentication = self.authentication.to_dict()

        constraints: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constraints, Unset):
            constraints = self.constraints.to_dict()

        shipping_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.shipping_address, Unset):
            shipping_address = self.shipping_address.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "design": design,
                "expiry": expiry,
                "externalRef": external_ref,
                "holder": holder,
                "limit": limit,
                "printedName": printed_name,
                "productCode": product_code,
            }
        )
        if authentication is not UNSET:
            field_dict["authentication"] = authentication
        if constraints is not UNSET:
            field_dict["constraints"] = constraints
        if shipping_address is not UNSET:
            field_dict["shippingAddress"] = shipping_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.card_address_detail import CardAddressDetail
        from ..models.card_card_authentication import CardCardAuthentication
        from ..models.card_card_holder import CardCardHolder
        from ..models.card_constraints import CardConstraints
        from ..models.card_product_design_detail import CardProductDesignDetail

        d = src_dict.copy()
        design = CardProductDesignDetail.from_dict(d.pop("design"))

        expiry = d.pop("expiry")

        external_ref = d.pop("externalRef")

        holder = CardCardHolder.from_dict(d.pop("holder"))

        limit = d.pop("limit")

        printed_name = d.pop("printedName")

        product_code = d.pop("productCode")

        _authentication = d.pop("authentication", UNSET)
        authentication: Union[Unset, CardCardAuthentication]
        if isinstance(_authentication, Unset):
            authentication = UNSET
        else:
            authentication = CardCardAuthentication.from_dict(_authentication)

        _constraints = d.pop("constraints", UNSET)
        constraints: Union[Unset, CardConstraints]
        if isinstance(_constraints, Unset):
            constraints = UNSET
        else:
            constraints = CardConstraints.from_dict(_constraints)

        _shipping_address = d.pop("shippingAddress", UNSET)
        shipping_address: Union[Unset, CardAddressDetail]
        if isinstance(_shipping_address, Unset):
            shipping_address = UNSET
        else:
            shipping_address = CardAddressDetail.from_dict(_shipping_address)

        card_create_physical_card_request = cls(
            design=design,
            expiry=expiry,
            external_ref=external_ref,
            holder=holder,
            limit=limit,
            printed_name=printed_name,
            product_code=product_code,
            authentication=authentication,
            constraints=constraints,
            shipping_address=shipping_address,
        )

        card_create_physical_card_request.additional_properties = d
        return card_create_physical_card_request

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
