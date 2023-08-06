import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.account_customer_legal_entity import AccountCustomerLegalEntity
from ..models.account_customer_status import AccountCustomerStatus
from ..models.account_customer_type import AccountCustomerType
from ..models.account_customer_verification_status import (
    AccountCustomerVerificationStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_response import AccountAddressResponse
    from ..models.account_associate_response import AccountAssociateResponse
    from ..models.account_brand_name_response import AccountBrandNameResponse
    from ..models.account_customer_tax_profile_response import (
        AccountCustomerTaxProfileResponse,
    )
    from ..models.account_customer_trust_response import AccountCustomerTrustResponse
    from ..models.account_delegate_response import AccountDelegateResponse
    from ..models.account_document_info import AccountDocumentInfo


T = TypeVar("T", bound="AccountCustomer")


@attr.s(auto_attribs=True)
class AccountCustomer:
    """A Customer is a single legal entity that can have 1 or more accounts

    Attributes:
        created_date (datetime.datetime): Datetime when the customer was created.Format is 'yyyy-MM-dd'T'HH:mm:ssZ'
            where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        id (str): Unique identifier for a Customer. Begins with 'C' Example: C00000001.
        name (str): Customer's company name - must be unique across the Modulr platform.
        status (AccountCustomerStatus): Status of the Customer. Customers must be 'Active' for Accounts to be created
            for them.
        type (AccountCustomerType): Type of the customer, can be one of:
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
        verification_status (AccountCustomerVerificationStatus): How the identity of the Customer has been verified. Can
            be:
            1. UNVERIFIED -> no verification checks have been completed
            2. VERIFIED -> verification checks completed satisfactorily
            3. EXVERIFIED -> verification completed externally
            4. REFERRED -> verification is pending manual review
            5. DECLINED -> verification is complete with a negative result
            6. REVIEWED -> verification check has been reviewed
        associates (Union[Unset, List['AccountAssociateResponse']]): Array of associate objects that link to the
            Customer. For example, this could contain the details of the company directors for a Limited company, or or the
            partners for a partnership.
        brand_names (Union[Unset, List['AccountBrandNameResponse']]): The customers brand name(s)
        company_reg_number (Union[Unset, str]): The company registration / incorporation number of the company. Only
            applicable for companies registered with Companies House
        customer_trust (Union[Unset, AccountCustomerTrustResponse]): Trust nature for customers of type trust. Mandatory
            for type Trust, not to be set for non-trust customers.
        delegate (Union[Unset, AccountDelegateResponse]): Delegate
        document_info (Union[Unset, List['AccountDocumentInfo']]): Array of document objects that relate to the Customer
            being created. Examples of Documents could be proof of a Company Director's identity or address, Articles of
            Association or a Partnership Agreement.
        expected_monthly_spend (Union[Unset, int]): Indication of the monthly spend of the customer.
        external_reference (Union[Unset, str]):
        industry_code (Union[Unset, str]):
        legal_entity (Union[Unset, AccountCustomerLegalEntity]): Legal entity of the customer
        partner_id (Union[Unset, str]): The owning partner identifier
        registered_address (Union[Unset, AccountAddressResponse]): Address
        tax_profile (Union[Unset, AccountCustomerTaxProfileResponse]): Tax profile for customers of type SOLETRADER.
            Optional for type SOLETRADER, not to be set for non-SOLETRADER customers.
        tcs_version (Union[Unset, int]): Version of the Modulr Account Terms and Conditions the Customer has agreed to.
        trading_address (Union[Unset, AccountAddressResponse]): Address
    """

    created_date: datetime.datetime
    id: str
    name: str
    status: AccountCustomerStatus
    type: AccountCustomerType
    verification_status: AccountCustomerVerificationStatus
    associates: Union[Unset, List["AccountAssociateResponse"]] = UNSET
    brand_names: Union[Unset, List["AccountBrandNameResponse"]] = UNSET
    company_reg_number: Union[Unset, str] = UNSET
    customer_trust: Union[Unset, "AccountCustomerTrustResponse"] = UNSET
    delegate: Union[Unset, "AccountDelegateResponse"] = UNSET
    document_info: Union[Unset, List["AccountDocumentInfo"]] = UNSET
    expected_monthly_spend: Union[Unset, int] = UNSET
    external_reference: Union[Unset, str] = UNSET
    industry_code: Union[Unset, str] = UNSET
    legal_entity: Union[Unset, AccountCustomerLegalEntity] = UNSET
    partner_id: Union[Unset, str] = UNSET
    registered_address: Union[Unset, "AccountAddressResponse"] = UNSET
    tax_profile: Union[Unset, "AccountCustomerTaxProfileResponse"] = UNSET
    tcs_version: Union[Unset, int] = UNSET
    trading_address: Union[Unset, "AccountAddressResponse"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_date = self.created_date.isoformat()

        id = self.id
        name = self.name
        status = self.status.value

        type = self.type.value

        verification_status = self.verification_status.value

        associates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.associates, Unset):
            associates = []
            for associates_item_data in self.associates:
                associates_item = associates_item_data.to_dict()

                associates.append(associates_item)

        brand_names: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.brand_names, Unset):
            brand_names = []
            for brand_names_item_data in self.brand_names:
                brand_names_item = brand_names_item_data.to_dict()

                brand_names.append(brand_names_item)

        company_reg_number = self.company_reg_number
        customer_trust: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.customer_trust, Unset):
            customer_trust = self.customer_trust.to_dict()

        delegate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delegate, Unset):
            delegate = self.delegate.to_dict()

        document_info: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.document_info, Unset):
            document_info = []
            for document_info_item_data in self.document_info:
                document_info_item = document_info_item_data.to_dict()

                document_info.append(document_info_item)

        expected_monthly_spend = self.expected_monthly_spend
        external_reference = self.external_reference
        industry_code = self.industry_code
        legal_entity: Union[Unset, str] = UNSET
        if not isinstance(self.legal_entity, Unset):
            legal_entity = self.legal_entity.value

        partner_id = self.partner_id
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
                "createdDate": created_date,
                "id": id,
                "name": name,
                "status": status,
                "type": type,
                "verificationStatus": verification_status,
            }
        )
        if associates is not UNSET:
            field_dict["associates"] = associates
        if brand_names is not UNSET:
            field_dict["brandNames"] = brand_names
        if company_reg_number is not UNSET:
            field_dict["companyRegNumber"] = company_reg_number
        if customer_trust is not UNSET:
            field_dict["customerTrust"] = customer_trust
        if delegate is not UNSET:
            field_dict["delegate"] = delegate
        if document_info is not UNSET:
            field_dict["documentInfo"] = document_info
        if expected_monthly_spend is not UNSET:
            field_dict["expectedMonthlySpend"] = expected_monthly_spend
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if industry_code is not UNSET:
            field_dict["industryCode"] = industry_code
        if legal_entity is not UNSET:
            field_dict["legalEntity"] = legal_entity
        if partner_id is not UNSET:
            field_dict["partnerId"] = partner_id
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
        from ..models.account_address_response import AccountAddressResponse
        from ..models.account_associate_response import AccountAssociateResponse
        from ..models.account_brand_name_response import AccountBrandNameResponse
        from ..models.account_customer_tax_profile_response import (
            AccountCustomerTaxProfileResponse,
        )
        from ..models.account_customer_trust_response import (
            AccountCustomerTrustResponse,
        )
        from ..models.account_delegate_response import AccountDelegateResponse
        from ..models.account_document_info import AccountDocumentInfo

        d = src_dict.copy()
        created_date = isoparse(d.pop("createdDate"))

        id = d.pop("id")

        name = d.pop("name")

        status = AccountCustomerStatus(d.pop("status"))

        type = AccountCustomerType(d.pop("type"))

        verification_status = AccountCustomerVerificationStatus(d.pop("verificationStatus"))

        associates = []
        _associates = d.pop("associates", UNSET)
        for associates_item_data in _associates or []:
            associates_item = AccountAssociateResponse.from_dict(associates_item_data)

            associates.append(associates_item)

        brand_names = []
        _brand_names = d.pop("brandNames", UNSET)
        for brand_names_item_data in _brand_names or []:
            brand_names_item = AccountBrandNameResponse.from_dict(brand_names_item_data)

            brand_names.append(brand_names_item)

        company_reg_number = d.pop("companyRegNumber", UNSET)

        _customer_trust = d.pop("customerTrust", UNSET)
        customer_trust: Union[Unset, AccountCustomerTrustResponse]
        if isinstance(_customer_trust, Unset):
            customer_trust = UNSET
        else:
            customer_trust = AccountCustomerTrustResponse.from_dict(_customer_trust)

        _delegate = d.pop("delegate", UNSET)
        delegate: Union[Unset, AccountDelegateResponse]
        if isinstance(_delegate, Unset):
            delegate = UNSET
        else:
            delegate = AccountDelegateResponse.from_dict(_delegate)

        document_info = []
        _document_info = d.pop("documentInfo", UNSET)
        for document_info_item_data in _document_info or []:
            document_info_item = AccountDocumentInfo.from_dict(document_info_item_data)

            document_info.append(document_info_item)

        expected_monthly_spend = d.pop("expectedMonthlySpend", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        industry_code = d.pop("industryCode", UNSET)

        _legal_entity = d.pop("legalEntity", UNSET)
        legal_entity: Union[Unset, AccountCustomerLegalEntity]
        if isinstance(_legal_entity, Unset):
            legal_entity = UNSET
        else:
            legal_entity = AccountCustomerLegalEntity(_legal_entity)

        partner_id = d.pop("partnerId", UNSET)

        _registered_address = d.pop("registeredAddress", UNSET)
        registered_address: Union[Unset, AccountAddressResponse]
        if isinstance(_registered_address, Unset):
            registered_address = UNSET
        else:
            registered_address = AccountAddressResponse.from_dict(_registered_address)

        _tax_profile = d.pop("taxProfile", UNSET)
        tax_profile: Union[Unset, AccountCustomerTaxProfileResponse]
        if isinstance(_tax_profile, Unset):
            tax_profile = UNSET
        else:
            tax_profile = AccountCustomerTaxProfileResponse.from_dict(_tax_profile)

        tcs_version = d.pop("tcsVersion", UNSET)

        _trading_address = d.pop("tradingAddress", UNSET)
        trading_address: Union[Unset, AccountAddressResponse]
        if isinstance(_trading_address, Unset):
            trading_address = UNSET
        else:
            trading_address = AccountAddressResponse.from_dict(_trading_address)

        account_customer = cls(
            created_date=created_date,
            id=id,
            name=name,
            status=status,
            type=type,
            verification_status=verification_status,
            associates=associates,
            brand_names=brand_names,
            company_reg_number=company_reg_number,
            customer_trust=customer_trust,
            delegate=delegate,
            document_info=document_info,
            expected_monthly_spend=expected_monthly_spend,
            external_reference=external_reference,
            industry_code=industry_code,
            legal_entity=legal_entity,
            partner_id=partner_id,
            registered_address=registered_address,
            tax_profile=tax_profile,
            tcs_version=tcs_version,
            trading_address=trading_address,
        )

        account_customer.additional_properties = d
        return account_customer

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
