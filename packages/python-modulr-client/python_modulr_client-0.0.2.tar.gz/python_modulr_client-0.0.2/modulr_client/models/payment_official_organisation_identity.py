from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentOfficialOrganisationIdentity")


@attr.s(auto_attribs=True)
class PaymentOfficialOrganisationIdentity:
    """Organisation's official identification. Official identification details. Property 'birthDetails' and/or
    'officialIdentification' Or 'officialIdDetailOrgs' is mandatory

        Attributes:
            bank_party_identification (Union[Unset, str]): Bank party identification Example: 12345.
            bei_identifier (Union[Unset, str]): BEI identification Example: MHIHISVZUMH.
            bic_identifier (Union[Unset, str]): BICI identification Example: MGALODJAO7A.
            central_bank_id_number (Union[Unset, str]): Central bank identification number Example: 678910.
            certificate_of_incorporation_number (Union[Unset, str]): Certification of the incorporation number Example:
                1100010.
            chips_universal_identifier (Union[Unset, str]): CHIPS universal identification Example: CH157373.
            clearing_id_number (Union[Unset, str]): Clearing identification Number Example: xx15402.
            country_id_code (Union[Unset, str]): Country identification code Example: 111111.
            customer_number (Union[Unset, str]): Customer number Example: 00221133.
            data_universal_numbering_system (Union[Unset, str]): Data universal numbering system Example: 002211330.
            eangln_identifier (Union[Unset, str]): EANGLN identification Example: 7516164953429.
            employer_id_number (Union[Unset, str]): Employer identification number Example: 00221133.
            generic_identification_3 (Union[Unset, str]): Generic identification 3 Example: 123456788.
            generic_identification_issr (Union[Unset, str]): Generic identification issr Example: 13143225.
            gs_1_gln_identifier (Union[Unset, str]): GS1GLN identifier Example: 00221133.
            ibei_identifier (Union[Unset, str]): IBEI identification Example: HIZFTMTT59.
            siren_code (Union[Unset, str]): SIREN code Example: 00221133.
            siret_code (Union[Unset, str]): SIRET code Example: 00221133.
            tax_id_number (Union[Unset, str]): Tax identification number Example: 00221133.
    """

    bank_party_identification: Union[Unset, str] = UNSET
    bei_identifier: Union[Unset, str] = UNSET
    bic_identifier: Union[Unset, str] = UNSET
    central_bank_id_number: Union[Unset, str] = UNSET
    certificate_of_incorporation_number: Union[Unset, str] = UNSET
    chips_universal_identifier: Union[Unset, str] = UNSET
    clearing_id_number: Union[Unset, str] = UNSET
    country_id_code: Union[Unset, str] = UNSET
    customer_number: Union[Unset, str] = UNSET
    data_universal_numbering_system: Union[Unset, str] = UNSET
    eangln_identifier: Union[Unset, str] = UNSET
    employer_id_number: Union[Unset, str] = UNSET
    generic_identification_3: Union[Unset, str] = UNSET
    generic_identification_issr: Union[Unset, str] = UNSET
    gs_1_gln_identifier: Union[Unset, str] = UNSET
    ibei_identifier: Union[Unset, str] = UNSET
    siren_code: Union[Unset, str] = UNSET
    siret_code: Union[Unset, str] = UNSET
    tax_id_number: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bank_party_identification = self.bank_party_identification
        bei_identifier = self.bei_identifier
        bic_identifier = self.bic_identifier
        central_bank_id_number = self.central_bank_id_number
        certificate_of_incorporation_number = self.certificate_of_incorporation_number
        chips_universal_identifier = self.chips_universal_identifier
        clearing_id_number = self.clearing_id_number
        country_id_code = self.country_id_code
        customer_number = self.customer_number
        data_universal_numbering_system = self.data_universal_numbering_system
        eangln_identifier = self.eangln_identifier
        employer_id_number = self.employer_id_number
        generic_identification_3 = self.generic_identification_3
        generic_identification_issr = self.generic_identification_issr
        gs_1_gln_identifier = self.gs_1_gln_identifier
        ibei_identifier = self.ibei_identifier
        siren_code = self.siren_code
        siret_code = self.siret_code
        tax_id_number = self.tax_id_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bank_party_identification is not UNSET:
            field_dict["bankPartyIdentification"] = bank_party_identification
        if bei_identifier is not UNSET:
            field_dict["beiIdentifier"] = bei_identifier
        if bic_identifier is not UNSET:
            field_dict["bicIdentifier"] = bic_identifier
        if central_bank_id_number is not UNSET:
            field_dict["centralBankIdNumber"] = central_bank_id_number
        if certificate_of_incorporation_number is not UNSET:
            field_dict["certificateOfIncorporationNumber"] = certificate_of_incorporation_number
        if chips_universal_identifier is not UNSET:
            field_dict["chipsUniversalIdentifier"] = chips_universal_identifier
        if clearing_id_number is not UNSET:
            field_dict["clearingIdNumber"] = clearing_id_number
        if country_id_code is not UNSET:
            field_dict["countryIdCode"] = country_id_code
        if customer_number is not UNSET:
            field_dict["customerNumber"] = customer_number
        if data_universal_numbering_system is not UNSET:
            field_dict["dataUniversalNumberingSystem"] = data_universal_numbering_system
        if eangln_identifier is not UNSET:
            field_dict["eanglnIdentifier"] = eangln_identifier
        if employer_id_number is not UNSET:
            field_dict["employerIdNumber"] = employer_id_number
        if generic_identification_3 is not UNSET:
            field_dict["genericIdentification3"] = generic_identification_3
        if generic_identification_issr is not UNSET:
            field_dict["genericIdentificationIssr"] = generic_identification_issr
        if gs_1_gln_identifier is not UNSET:
            field_dict["gs1glnIdentifier"] = gs_1_gln_identifier
        if ibei_identifier is not UNSET:
            field_dict["ibeiIdentifier"] = ibei_identifier
        if siren_code is not UNSET:
            field_dict["sirenCode"] = siren_code
        if siret_code is not UNSET:
            field_dict["siretCode"] = siret_code
        if tax_id_number is not UNSET:
            field_dict["taxIdNumber"] = tax_id_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bank_party_identification = d.pop("bankPartyIdentification", UNSET)

        bei_identifier = d.pop("beiIdentifier", UNSET)

        bic_identifier = d.pop("bicIdentifier", UNSET)

        central_bank_id_number = d.pop("centralBankIdNumber", UNSET)

        certificate_of_incorporation_number = d.pop("certificateOfIncorporationNumber", UNSET)

        chips_universal_identifier = d.pop("chipsUniversalIdentifier", UNSET)

        clearing_id_number = d.pop("clearingIdNumber", UNSET)

        country_id_code = d.pop("countryIdCode", UNSET)

        customer_number = d.pop("customerNumber", UNSET)

        data_universal_numbering_system = d.pop("dataUniversalNumberingSystem", UNSET)

        eangln_identifier = d.pop("eanglnIdentifier", UNSET)

        employer_id_number = d.pop("employerIdNumber", UNSET)

        generic_identification_3 = d.pop("genericIdentification3", UNSET)

        generic_identification_issr = d.pop("genericIdentificationIssr", UNSET)

        gs_1_gln_identifier = d.pop("gs1glnIdentifier", UNSET)

        ibei_identifier = d.pop("ibeiIdentifier", UNSET)

        siren_code = d.pop("sirenCode", UNSET)

        siret_code = d.pop("siretCode", UNSET)

        tax_id_number = d.pop("taxIdNumber", UNSET)

        payment_official_organisation_identity = cls(
            bank_party_identification=bank_party_identification,
            bei_identifier=bei_identifier,
            bic_identifier=bic_identifier,
            central_bank_id_number=central_bank_id_number,
            certificate_of_incorporation_number=certificate_of_incorporation_number,
            chips_universal_identifier=chips_universal_identifier,
            clearing_id_number=clearing_id_number,
            country_id_code=country_id_code,
            customer_number=customer_number,
            data_universal_numbering_system=data_universal_numbering_system,
            eangln_identifier=eangln_identifier,
            employer_id_number=employer_id_number,
            generic_identification_3=generic_identification_3,
            generic_identification_issr=generic_identification_issr,
            gs_1_gln_identifier=gs_1_gln_identifier,
            ibei_identifier=ibei_identifier,
            siren_code=siren_code,
            siret_code=siret_code,
            tax_id_number=tax_id_number,
        )

        payment_official_organisation_identity.additional_properties = d
        return payment_official_organisation_identity

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
