from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.account_create_customer_request_legal_entity import (
    AccountCreateCustomerRequestLegalEntity,
)
from ..models.account_create_customer_request_type import (
    AccountCreateCustomerRequestType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_request import AccountAddressRequest
    from ..models.account_create_associate_request import AccountCreateAssociateRequest
    from ..models.account_customer_tax_profile_request import (
        AccountCustomerTaxProfileRequest,
    )
    from ..models.account_customer_trust_request import AccountCustomerTrustRequest
    from ..models.account_document_info import AccountDocumentInfo


T = TypeVar("T", bound="AccountCreateCustomerRequest")


@attr.s(auto_attribs=True)
class AccountCreateCustomerRequest:
    r"""Details of customer to create

    Attributes:
        legal_entity (AccountCreateCustomerRequestLegalEntity): Legal entity of the customer
        type (AccountCreateCustomerRequestType): Type of the customer, can be one of:
            1. LLC -> limited company
            2. PLC -> publicly listed company
            3. SOLETRADER -> sole trader
            4. OPARTNRSHP -> ordinary partnership
            5. LPARTNRSHP -> limited partnership
            6. LLP -> limited liability partnership
            7. CHARITY -> charity
            8. INDIVIDUAL -> individual consumer
            9. PCM_INDIVIDUAL -> partner clearing model individual consumer
            10. PCM_BUSINESS -> partner clearing model business consumer
            11. TRUST -> trust customer
        associates (Union[Unset, List['AccountCreateAssociateRequest']]): Mandatory for all types except 'PCM_BUSINESS'
        company_reg_number (Union[Unset, str]): Company registration number. Mandatory for 'LLC' and 'PLC'
        customer_trust (Union[Unset, AccountCustomerTrustRequest]): Trust nature for customers of type Trust. Mandatory
            for type Trust, not to be set for non-trust customers.
        document_info (Union[Unset, List['AccountDocumentInfo']]): information on uploaded documents
        expected_monthly_spend (Union[Unset, int]): Mandatory for all types except 'PCM_INDIVIDUAL' and 'PCM_BUSINESS'
        external_reference (Union[Unset, str]): External Reference can only have alphanumeric characters plus
            underscore, hyphen and space up to 50 characters long
        industry_code (Union[Unset, str]): Mandatory for all types except 'INDIVIDUAL', 'PCM_INDIVIDUAL' and
            'PCM_BUSINESS'
        name (Union[Unset, str]): AlphaNumeric characters plus [ _ ' @ , & £ $ € ¥ = # % ‘ ’ : ; \ / < > « »  ! ‘ “ ” .
            ? - *{ }  + % ( )]. Mandatory for all types except 'INDIVIDUAL and PCM_INDIVIDUAL'
        provisional_customer_id (Union[Unset, str]): Reference to provisional customer in onboarding flow
        registered_address (Union[Unset, AccountAddressRequest]): Applicable to all types except 'INDIVIDUAL' and
            'PCM_INDIVIDUAL'
        tax_profile (Union[Unset, AccountCustomerTaxProfileRequest]): Tax profile for customers of type SOLETRADER.
            Optional for type SOLETRADER, not to be set for non-SOLETRADER customers.
        tcs_version (Union[Unset, int]): Terms and conditions version. Mandatory for all types except 'PCM_INDIVIDUAL'
            and 'PCM_BUSINESS'
        trading_address (Union[Unset, AccountAddressRequest]): Applicable to all types except 'INDIVIDUAL' and
            'PCM_INDIVIDUAL'
    """

    legal_entity: AccountCreateCustomerRequestLegalEntity
    type: AccountCreateCustomerRequestType
    associates: Union[Unset, List["AccountCreateAssociateRequest"]] = UNSET
    company_reg_number: Union[Unset, str] = UNSET
    customer_trust: Union[Unset, "AccountCustomerTrustRequest"] = UNSET
    document_info: Union[Unset, List["AccountDocumentInfo"]] = UNSET
    expected_monthly_spend: Union[Unset, int] = UNSET
    external_reference: Union[Unset, str] = UNSET
    industry_code: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    provisional_customer_id: Union[Unset, str] = UNSET
    registered_address: Union[Unset, "AccountAddressRequest"] = UNSET
    tax_profile: Union[Unset, "AccountCustomerTaxProfileRequest"] = UNSET
    tcs_version: Union[Unset, int] = UNSET
    trading_address: Union[Unset, "AccountAddressRequest"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        legal_entity = self.legal_entity.value

        type = self.type.value

        associates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.associates, Unset):
            associates = []
            for associates_item_data in self.associates:
                associates_item = associates_item_data.to_dict()

                associates.append(associates_item)

        company_reg_number = self.company_reg_number
        customer_trust: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.customer_trust, Unset):
            customer_trust = self.customer_trust.to_dict()

        document_info: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.document_info, Unset):
            document_info = []
            for document_info_item_data in self.document_info:
                document_info_item = document_info_item_data.to_dict()

                document_info.append(document_info_item)

        expected_monthly_spend = self.expected_monthly_spend
        external_reference = self.external_reference
        industry_code = self.industry_code
        name = self.name
        provisional_customer_id = self.provisional_customer_id
        registered_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.registered_address, Unset):
            registered_address = self.registered_address.to_dict()

        tax_profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tax_profile, Unset):
            tax_profile = self.tax_profile.to_dict()

        tcs_version = self.tcs_version
        trading_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trading_address, Unset):
            trading_address = self.trading_address.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "legalEntity": legal_entity,
                "type": type,
            }
        )
        if associates is not UNSET:
            field_dict["associates"] = associates
        if company_reg_number is not UNSET:
            field_dict["companyRegNumber"] = company_reg_number
        if customer_trust is not UNSET:
            field_dict["customerTrust"] = customer_trust
        if document_info is not UNSET:
            field_dict["documentInfo"] = document_info
        if expected_monthly_spend is not UNSET:
            field_dict["expectedMonthlySpend"] = expected_monthly_spend
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if industry_code is not UNSET:
            field_dict["industryCode"] = industry_code
        if name is not UNSET:
            field_dict["name"] = name
        if provisional_customer_id is not UNSET:
            field_dict["provisionalCustomerId"] = provisional_customer_id
        if registered_address is not UNSET:
            field_dict["registeredAddress"] = registered_address
        if tax_profile is not UNSET:
            field_dict["taxProfile"] = tax_profile
        if tcs_version is not UNSET:
            field_dict["tcsVersion"] = tcs_version
        if trading_address is not UNSET:
            field_dict["tradingAddress"] = trading_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_address_request import AccountAddressRequest
        from ..models.account_create_associate_request import (
            AccountCreateAssociateRequest,
        )
        from ..models.account_customer_tax_profile_request import (
            AccountCustomerTaxProfileRequest,
        )
        from ..models.account_customer_trust_request import AccountCustomerTrustRequest
        from ..models.account_document_info import AccountDocumentInfo

        d = src_dict.copy()
        legal_entity = AccountCreateCustomerRequestLegalEntity(d.pop("legalEntity"))

        type = AccountCreateCustomerRequestType(d.pop("type"))

        associates = []
        _associates = d.pop("associates", UNSET)
        for associates_item_data in _associates or []:
            associates_item = AccountCreateAssociateRequest.from_dict(associates_item_data)

            associates.append(associates_item)

        company_reg_number = d.pop("companyRegNumber", UNSET)

        _customer_trust = d.pop("customerTrust", UNSET)
        customer_trust: Union[Unset, AccountCustomerTrustRequest]
        if isinstance(_customer_trust, Unset):
            customer_trust = UNSET
        else:
            customer_trust = AccountCustomerTrustRequest.from_dict(_customer_trust)

        document_info = []
        _document_info = d.pop("documentInfo", UNSET)
        for document_info_item_data in _document_info or []:
            document_info_item = AccountDocumentInfo.from_dict(document_info_item_data)

            document_info.append(document_info_item)

        expected_monthly_spend = d.pop("expectedMonthlySpend", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        industry_code = d.pop("industryCode", UNSET)

        name = d.pop("name", UNSET)

        provisional_customer_id = d.pop("provisionalCustomerId", UNSET)

        _registered_address = d.pop("registeredAddress", UNSET)
        registered_address: Union[Unset, AccountAddressRequest]
        if isinstance(_registered_address, Unset):
            registered_address = UNSET
        else:
            registered_address = AccountAddressRequest.from_dict(_registered_address)

        _tax_profile = d.pop("taxProfile", UNSET)
        tax_profile: Union[Unset, AccountCustomerTaxProfileRequest]
        if isinstance(_tax_profile, Unset):
            tax_profile = UNSET
        else:
            tax_profile = AccountCustomerTaxProfileRequest.from_dict(_tax_profile)

        tcs_version = d.pop("tcsVersion", UNSET)

        _trading_address = d.pop("tradingAddress", UNSET)
        trading_address: Union[Unset, AccountAddressRequest]
        if isinstance(_trading_address, Unset):
            trading_address = UNSET
        else:
            trading_address = AccountAddressRequest.from_dict(_trading_address)

        account_create_customer_request = cls(
            legal_entity=legal_entity,
            type=type,
            associates=associates,
            company_reg_number=company_reg_number,
            customer_trust=customer_trust,
            document_info=document_info,
            expected_monthly_spend=expected_monthly_spend,
            external_reference=external_reference,
            industry_code=industry_code,
            name=name,
            provisional_customer_id=provisional_customer_id,
            registered_address=registered_address,
            tax_profile=tax_profile,
            tcs_version=tcs_version,
            trading_address=trading_address,
        )

        account_create_customer_request.additional_properties = d
        return account_create_customer_request

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
