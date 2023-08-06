from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_create_associate_request_type import (
    AccountCreateAssociateRequestType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_additional_associate_identifier import (
        AccountAdditionalAssociateIdentifier,
    )
    from ..models.account_address_request import AccountAddressRequest
    from ..models.account_associate_compliance_data_request import (
        AccountAssociateComplianceDataRequest,
    )
    from ..models.account_document_info import AccountDocumentInfo


T = TypeVar("T", bound="AccountCreateAssociateRequest")


@attr.s(auto_attribs=True)
class AccountCreateAssociateRequest:
    """Mandatory for all types except 'PCM_BUSINESS'

    Attributes:
        first_name (str): Letters, hyphens and apostrophes
        home_address (AccountAddressRequest): Applicable to all types except 'INDIVIDUAL' and 'PCM_INDIVIDUAL'
        last_name (str): Letters, hyphens and apostrophes
        type (AccountCreateAssociateRequestType): Type of associate
        additional_identifiers (Union[Unset, List['AccountAdditionalAssociateIdentifier']]): Additional identifiers
        applicant (Union[Unset, bool]): Indicates if the associate is the applicant. Only one associate can be marked as
            such.
        compliance_data (Union[Unset, AccountAssociateComplianceDataRequest]): Optional for associates of type
            C_INTEREST and an EU customer legal entity. Not to be set for other associate types and/or for UK customer legal
            entity.
        date_of_birth (Union[Unset, str]): Date in yyyy-MM-dd format. If associate is a non-applicant director or
            partner, then partial DOB of yyyy-MM format is allowed. Valid age is from 16 to 100 years. If Applicant then
            minimum age required is 18 years for specific partners. Required for all associate types except PCM_INDIVIDUAL.
        document_info (Union[Unset, List['AccountDocumentInfo']]): Information on uploaded documents
        email (Union[Unset, str]): Contact email address for applicants
        middle_name (Union[Unset, str]): Letters, hyphens and apostrophes
        ownership (Union[Unset, int]): Ownership percentage for Partners
        phone (Union[Unset, str]): Contact phone number for applicants, will be formatted into international number
            pattern
    """

    first_name: str
    home_address: "AccountAddressRequest"
    last_name: str
    type: AccountCreateAssociateRequestType
    additional_identifiers: Union[Unset, List["AccountAdditionalAssociateIdentifier"]] = UNSET
    applicant: Union[Unset, bool] = UNSET
    compliance_data: Union[Unset, "AccountAssociateComplianceDataRequest"] = UNSET
    date_of_birth: Union[Unset, str] = UNSET
    document_info: Union[Unset, List["AccountDocumentInfo"]] = UNSET
    email: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    ownership: Union[Unset, int] = UNSET
    phone: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        home_address = self.home_address.to_dict()

        last_name = self.last_name
        type = self.type.value

        additional_identifiers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.additional_identifiers, Unset):
            additional_identifiers = []
            for additional_identifiers_item_data in self.additional_identifiers:
                additional_identifiers_item = additional_identifiers_item_data.to_dict()

                additional_identifiers.append(additional_identifiers_item)

        applicant = self.applicant
        compliance_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.compliance_data, Unset):
            compliance_data = self.compliance_data.to_dict()

        date_of_birth = self.date_of_birth
        document_info: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.document_info, Unset):
            document_info = []
            for document_info_item_data in self.document_info:
                document_info_item = document_info_item_data.to_dict()

                document_info.append(document_info_item)

        email = self.email
        middle_name = self.middle_name
        ownership = self.ownership
        phone = self.phone

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "firstName": first_name,
                "homeAddress": home_address,
                "lastName": last_name,
                "type": type,
            }
        )
        if additional_identifiers is not UNSET:
            field_dict["additionalIdentifiers"] = additional_identifiers
        if applicant is not UNSET:
            field_dict["applicant"] = applicant
        if compliance_data is not UNSET:
            field_dict["complianceData"] = compliance_data
        if date_of_birth is not UNSET:
            field_dict["dateOfBirth"] = date_of_birth
        if document_info is not UNSET:
            field_dict["documentInfo"] = document_info
        if email is not UNSET:
            field_dict["email"] = email
        if middle_name is not UNSET:
            field_dict["middleName"] = middle_name
        if ownership is not UNSET:
            field_dict["ownership"] = ownership
        if phone is not UNSET:
            field_dict["phone"] = phone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_additional_associate_identifier import (
            AccountAdditionalAssociateIdentifier,
        )
        from ..models.account_address_request import AccountAddressRequest
        from ..models.account_associate_compliance_data_request import (
            AccountAssociateComplianceDataRequest,
        )
        from ..models.account_document_info import AccountDocumentInfo

        d = src_dict.copy()
        first_name = d.pop("firstName")

        home_address = AccountAddressRequest.from_dict(d.pop("homeAddress"))

        last_name = d.pop("lastName")

        type = AccountCreateAssociateRequestType(d.pop("type"))

        additional_identifiers = []
        _additional_identifiers = d.pop("additionalIdentifiers", UNSET)
        for additional_identifiers_item_data in _additional_identifiers or []:
            additional_identifiers_item = AccountAdditionalAssociateIdentifier.from_dict(
                additional_identifiers_item_data
            )

            additional_identifiers.append(additional_identifiers_item)

        applicant = d.pop("applicant", UNSET)

        _compliance_data = d.pop("complianceData", UNSET)
        compliance_data: Union[Unset, AccountAssociateComplianceDataRequest]
        if isinstance(_compliance_data, Unset):
            compliance_data = UNSET
        else:
            compliance_data = AccountAssociateComplianceDataRequest.from_dict(_compliance_data)

        date_of_birth = d.pop("dateOfBirth", UNSET)

        document_info = []
        _document_info = d.pop("documentInfo", UNSET)
        for document_info_item_data in _document_info or []:
            document_info_item = AccountDocumentInfo.from_dict(document_info_item_data)

            document_info.append(document_info_item)

        email = d.pop("email", UNSET)

        middle_name = d.pop("middleName", UNSET)

        ownership = d.pop("ownership", UNSET)

        phone = d.pop("phone", UNSET)

        account_create_associate_request = cls(
            first_name=first_name,
            home_address=home_address,
            last_name=last_name,
            type=type,
            additional_identifiers=additional_identifiers,
            applicant=applicant,
            compliance_data=compliance_data,
            date_of_birth=date_of_birth,
            document_info=document_info,
            email=email,
            middle_name=middle_name,
            ownership=ownership,
            phone=phone,
        )

        account_create_associate_request.additional_properties = d
        return account_create_associate_request

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
