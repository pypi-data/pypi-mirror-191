from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_address import PaymentAddress
    from ..models.payment_birth_details import PaymentBirthDetails
    from ..models.payment_official_id_details import PaymentOfficialIdDetails
    from ..models.payment_official_organisation_identity import (
        PaymentOfficialOrganisationIdentity,
    )
    from ..models.payment_overseas_account_identifier import (
        PaymentOverseasAccountIdentifier,
    )


T = TypeVar("T", bound="PaymentUltimatePayer")


@attr.s(auto_attribs=True)
class PaymentUltimatePayer:
    """
    Attributes:
        address (PaymentAddress):
        name (str): Name of the ultimate payer
        bic (Union[Unset, str]): Destination beneficiary's BIC/Swift Code. Example: MODRDEFF123.
        birth_details (Union[Unset, PaymentBirthDetails]): Birth details of a person. Official identification details.
            Property 'birthDetails' and/or 'officialIdentification' Or 'officialIdDetailOrgs' is mandatory
        official_id_detail_orgs (Union[Unset, PaymentOfficialOrganisationIdentity]): Organisation's official
            identification. Official identification details. Property 'birthDetails' and/or 'officialIdentification' Or
            'officialIdDetailOrgs' is mandatory
        official_identification (Union[Unset, PaymentOfficialIdDetails]): Official identification for a person. Property
            'birthDetails' and/or 'officialIdentification' Or 'officialIdDetailOrgs' is mandatory
        overseas_account_identifier (Union[Unset, PaymentOverseasAccountIdentifier]):
    """

    address: "PaymentAddress"
    name: str
    bic: Union[Unset, str] = UNSET
    birth_details: Union[Unset, "PaymentBirthDetails"] = UNSET
    official_id_detail_orgs: Union[Unset, "PaymentOfficialOrganisationIdentity"] = UNSET
    official_identification: Union[Unset, "PaymentOfficialIdDetails"] = UNSET
    overseas_account_identifier: Union[Unset, "PaymentOverseasAccountIdentifier"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address.to_dict()

        name = self.name
        bic = self.bic
        birth_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.birth_details, Unset):
            birth_details = self.birth_details.to_dict()

        official_id_detail_orgs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.official_id_detail_orgs, Unset):
            official_id_detail_orgs = self.official_id_detail_orgs.to_dict()

        official_identification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.official_identification, Unset):
            official_identification = self.official_identification.to_dict()

        overseas_account_identifier: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.overseas_account_identifier, Unset):
            overseas_account_identifier = self.overseas_account_identifier.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "name": name,
            }
        )
        if bic is not UNSET:
            field_dict["bic"] = bic
        if birth_details is not UNSET:
            field_dict["birthDetails"] = birth_details
        if official_id_detail_orgs is not UNSET:
            field_dict["officialIdDetailOrgs"] = official_id_detail_orgs
        if official_identification is not UNSET:
            field_dict["officialIdentification"] = official_identification
        if overseas_account_identifier is not UNSET:
            field_dict["overseasAccountIdentifier"] = overseas_account_identifier

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_address import PaymentAddress
        from ..models.payment_birth_details import PaymentBirthDetails
        from ..models.payment_official_id_details import PaymentOfficialIdDetails
        from ..models.payment_official_organisation_identity import (
            PaymentOfficialOrganisationIdentity,
        )
        from ..models.payment_overseas_account_identifier import (
            PaymentOverseasAccountIdentifier,
        )

        d = src_dict.copy()
        address = PaymentAddress.from_dict(d.pop("address"))

        name = d.pop("name")

        bic = d.pop("bic", UNSET)

        _birth_details = d.pop("birthDetails", UNSET)
        birth_details: Union[Unset, PaymentBirthDetails]
        if isinstance(_birth_details, Unset):
            birth_details = UNSET
        else:
            birth_details = PaymentBirthDetails.from_dict(_birth_details)

        _official_id_detail_orgs = d.pop("officialIdDetailOrgs", UNSET)
        official_id_detail_orgs: Union[Unset, PaymentOfficialOrganisationIdentity]
        if isinstance(_official_id_detail_orgs, Unset):
            official_id_detail_orgs = UNSET
        else:
            official_id_detail_orgs = PaymentOfficialOrganisationIdentity.from_dict(
                _official_id_detail_orgs
            )

        _official_identification = d.pop("officialIdentification", UNSET)
        official_identification: Union[Unset, PaymentOfficialIdDetails]
        if isinstance(_official_identification, Unset):
            official_identification = UNSET
        else:
            official_identification = PaymentOfficialIdDetails.from_dict(_official_identification)

        _overseas_account_identifier = d.pop("overseasAccountIdentifier", UNSET)
        overseas_account_identifier: Union[Unset, PaymentOverseasAccountIdentifier]
        if isinstance(_overseas_account_identifier, Unset):
            overseas_account_identifier = UNSET
        else:
            overseas_account_identifier = PaymentOverseasAccountIdentifier.from_dict(
                _overseas_account_identifier
            )

        payment_ultimate_payer = cls(
            address=address,
            name=name,
            bic=bic,
            birth_details=birth_details,
            official_id_detail_orgs=official_id_detail_orgs,
            official_identification=official_identification,
            overseas_account_identifier=overseas_account_identifier,
        )

        payment_ultimate_payer.additional_properties = d
        return payment_ultimate_payer

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
