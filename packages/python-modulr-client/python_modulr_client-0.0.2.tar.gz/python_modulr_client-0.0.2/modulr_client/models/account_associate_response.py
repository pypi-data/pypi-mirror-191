from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_associate_response_type import AccountAssociateResponseType
from ..models.account_associate_response_verification_status import (
    AccountAssociateResponseVerificationStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_additional_personal_identifier_response import (
        AccountAdditionalPersonalIdentifierResponse,
    )
    from ..models.account_address_response import AccountAddressResponse
    from ..models.account_associate_compliance_data_response import (
        AccountAssociateComplianceDataResponse,
    )
    from ..models.account_document_info import AccountDocumentInfo


T = TypeVar("T", bound="AccountAssociateResponse")


@attr.s(auto_attribs=True)
class AccountAssociateResponse:
    """Associate

    Attributes:
        date_of_birth (str): Associate's date of birth in format yyyy-MM-dd, or format yyyy-MM where day is unknown
        first_name (str): Associate's first name(s)
        id (str): Unique id for the Associate
        last_name (str): Associate's surname
        type (AccountAssociateResponseType): Describes the relation between the Associate and the Customer. Can be one
            of DIRECTOR, PARTNER, CSECRETARY, SOLETRADER, BENE_OWNER, C_INTEREST, INDIVIDUAL, PCM_INDIVIDUAL, SIGNATORY,
            TRUST_SETTLOR, TRUST_BENEFICIARY, TRUST_TRUSTEE
        verification_status (AccountAssociateResponseVerificationStatus): How the Associate was verified. Can be one of
            UNVERIFIED, VERIFIED, EXVERIFIED, REFERRED, DECLINED, REVIEWED, MIGRATED
        additional_personal_identifiers (Union[Unset, List['AccountAdditionalPersonalIdentifierResponse']]): Additional
            personal identifier(s)
        applicant (Union[Unset, bool]): Indicates which Associate originally applied for the Modulr account
        compliance_data (Union[Unset, AccountAssociateComplianceDataResponse]): Optional for associates of type
            C_INTEREST and an EU customer legal entity. Not to be set for other associate types and/or for UK customer legal
            entity.
        document_info (Union[Unset, List['AccountDocumentInfo']]): Documents gathered during Customer Due Diligence
            checks on an Associate.
        email (Union[Unset, str]): Associate's email address
        home_address (Union[Unset, AccountAddressResponse]): Address
        middle_name (Union[Unset, str]): Associate's middle name
        ownership (Union[Unset, int]): The Associate's percentage ownership of the Customer
        phone (Union[Unset, str]): Associate's phone number, in international number format
    """

    date_of_birth: str
    first_name: str
    id: str
    last_name: str
    type: AccountAssociateResponseType
    verification_status: AccountAssociateResponseVerificationStatus
    additional_personal_identifiers: Union[
        Unset, List["AccountAdditionalPersonalIdentifierResponse"]
    ] = UNSET
    applicant: Union[Unset, bool] = UNSET
    compliance_data: Union[Unset, "AccountAssociateComplianceDataResponse"] = UNSET
    document_info: Union[Unset, List["AccountDocumentInfo"]] = UNSET
    email: Union[Unset, str] = UNSET
    home_address: Union[Unset, "AccountAddressResponse"] = UNSET
    middle_name: Union[Unset, str] = UNSET
    ownership: Union[Unset, int] = UNSET
    phone: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        date_of_birth = self.date_of_birth
        first_name = self.first_name
        id = self.id
        last_name = self.last_name
        type = self.type.value

        verification_status = self.verification_status.value

        additional_personal_identifiers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.additional_personal_identifiers, Unset):
            additional_personal_identifiers = []
            for additional_personal_identifiers_item_data in self.additional_personal_identifiers:
                additional_personal_identifiers_item = (
                    additional_personal_identifiers_item_data.to_dict()
                )

                additional_personal_identifiers.append(additional_personal_identifiers_item)

        applicant = self.applicant
        compliance_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.compliance_data, Unset):
            compliance_data = self.compliance_data.to_dict()

        document_info: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.document_info, Unset):
            document_info = []
            for document_info_item_data in self.document_info:
                document_info_item = document_info_item_data.to_dict()

                document_info.append(document_info_item)

        email = self.email
        home_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.home_address, Unset):
            home_address = self.home_address.to_dict()

        middle_name = self.middle_name
        ownership = self.ownership
        phone = self.phone

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dateOfBirth": date_of_birth,
                "firstName": first_name,
                "id": id,
                "lastName": last_name,
                "type": type,
                "verificationStatus": verification_status,
            }
        )
        if additional_personal_identifiers is not UNSET:
            field_dict["additionalPersonalIdentifiers"] = additional_personal_identifiers
        if applicant is not UNSET:
            field_dict["applicant"] = applicant
        if compliance_data is not UNSET:
            field_dict["complianceData"] = compliance_data
        if document_info is not UNSET:
            field_dict["documentInfo"] = document_info
        if email is not UNSET:
            field_dict["email"] = email
        if home_address is not UNSET:
            field_dict["homeAddress"] = home_address
        if middle_name is not UNSET:
            field_dict["middleName"] = middle_name
        if ownership is not UNSET:
            field_dict["ownership"] = ownership
        if phone is not UNSET:
            field_dict["phone"] = phone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_additional_personal_identifier_response import (
            AccountAdditionalPersonalIdentifierResponse,
        )
        from ..models.account_address_response import AccountAddressResponse
        from ..models.account_associate_compliance_data_response import (
            AccountAssociateComplianceDataResponse,
        )
        from ..models.account_document_info import AccountDocumentInfo

        d = src_dict.copy()
        date_of_birth = d.pop("dateOfBirth")

        first_name = d.pop("firstName")

        id = d.pop("id")

        last_name = d.pop("lastName")

        type = AccountAssociateResponseType(d.pop("type"))

        verification_status = AccountAssociateResponseVerificationStatus(
            d.pop("verificationStatus")
        )

        additional_personal_identifiers = []
        _additional_personal_identifiers = d.pop("additionalPersonalIdentifiers", UNSET)
        for additional_personal_identifiers_item_data in _additional_personal_identifiers or []:
            additional_personal_identifiers_item = (
                AccountAdditionalPersonalIdentifierResponse.from_dict(
                    additional_personal_identifiers_item_data
                )
            )

            additional_personal_identifiers.append(additional_personal_identifiers_item)

        applicant = d.pop("applicant", UNSET)

        _compliance_data = d.pop("complianceData", UNSET)
        compliance_data: Union[Unset, AccountAssociateComplianceDataResponse]
        if isinstance(_compliance_data, Unset):
            compliance_data = UNSET
        else:
            compliance_data = AccountAssociateComplianceDataResponse.from_dict(_compliance_data)

        document_info = []
        _document_info = d.pop("documentInfo", UNSET)
        for document_info_item_data in _document_info or []:
            document_info_item = AccountDocumentInfo.from_dict(document_info_item_data)

            document_info.append(document_info_item)

        email = d.pop("email", UNSET)

        _home_address = d.pop("homeAddress", UNSET)
        home_address: Union[Unset, AccountAddressResponse]
        if isinstance(_home_address, Unset):
            home_address = UNSET
        else:
            home_address = AccountAddressResponse.from_dict(_home_address)

        middle_name = d.pop("middleName", UNSET)

        ownership = d.pop("ownership", UNSET)

        phone = d.pop("phone", UNSET)

        account_associate_response = cls(
            date_of_birth=date_of_birth,
            first_name=first_name,
            id=id,
            last_name=last_name,
            type=type,
            verification_status=verification_status,
            additional_personal_identifiers=additional_personal_identifiers,
            applicant=applicant,
            compliance_data=compliance_data,
            document_info=document_info,
            email=email,
            home_address=home_address,
            middle_name=middle_name,
            ownership=ownership,
            phone=phone,
        )

        account_associate_response.additional_properties = d
        return account_associate_response

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
