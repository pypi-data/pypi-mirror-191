import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.account_beneficiary_response_approval_status import (
    AccountBeneficiaryResponseApprovalStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_address_response import AccountAddressResponse
    from ..models.account_identifier_response import AccountIdentifierResponse


T = TypeVar("T", bound="AccountBeneficiaryResponse")


@attr.s(auto_attribs=True)
class AccountBeneficiaryResponse:
    """Beneficiary

    Attributes:
        created (datetime.datetime): Datetime the Beneficiary was created.Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is
            UTC offset. e.g 2017-01-28T01:01:01+0000
        customer_id (str): Id of the customer than owns this beneficiary Example: C0000001.
        default_reference (str): Default reference used for payments to the Beneficiary.
        destination_identifier (AccountIdentifierResponse): Account Identifier
        id (str): Unique reference for the Beneficiary. Example: B00000001A.
        name (str): Name for the Beneficiary
        status (str): Status of the Beneficiary. Can be:
        updated (datetime.datetime): Datetime the Beneficiary was last updated.Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where
            Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        access_groups (Union[Unset, List[str]]): Access groups associated with beneficiary.
        account_id (Union[Unset, str]): Id of the account if this beneficiary is a Modulr account, null otherwise
        address (Union[Unset, AccountAddressResponse]): Address
        approval_request_id (Union[Unset, str]): Approval request ID for pending records.
        approval_required (Union[Unset, bool]): Indicates if the beneficiary creation is pending approval
        approval_status (Union[Unset, AccountBeneficiaryResponseApprovalStatus]): Approval status of item.
        birthdate (Union[Unset, datetime.date]): Date of birth for the Beneficiary in yyyy-MM-dd format
        email_address (Union[Unset, str]): Email address for the Beneficiary
        external_reference (Union[Unset, str]): External system reference for the Beneficiary
        phone_number (Union[Unset, str]): Phone number for the Beneficiary in international pattern
        qualifier (Union[Unset, str]): Qualifier for this beneficiary
        redirected_destination (Union[Unset, AccountIdentifierResponse]): Account Identifier
    """

    created: datetime.datetime
    customer_id: str
    default_reference: str
    destination_identifier: "AccountIdentifierResponse"
    id: str
    name: str
    status: str
    updated: datetime.datetime
    access_groups: Union[Unset, List[str]] = UNSET
    account_id: Union[Unset, str] = UNSET
    address: Union[Unset, "AccountAddressResponse"] = UNSET
    approval_request_id: Union[Unset, str] = UNSET
    approval_required: Union[Unset, bool] = UNSET
    approval_status: Union[Unset, AccountBeneficiaryResponseApprovalStatus] = UNSET
    birthdate: Union[Unset, datetime.date] = UNSET
    email_address: Union[Unset, str] = UNSET
    external_reference: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    qualifier: Union[Unset, str] = UNSET
    redirected_destination: Union[Unset, "AccountIdentifierResponse"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created = self.created.isoformat()

        customer_id = self.customer_id
        default_reference = self.default_reference
        destination_identifier = self.destination_identifier.to_dict()

        id = self.id
        name = self.name
        status = self.status
        updated = self.updated.isoformat()

        access_groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.access_groups, Unset):
            access_groups = self.access_groups

        account_id = self.account_id
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        approval_request_id = self.approval_request_id
        approval_required = self.approval_required
        approval_status: Union[Unset, str] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        birthdate: Union[Unset, str] = UNSET
        if not isinstance(self.birthdate, Unset):
            birthdate = self.birthdate.isoformat()

        email_address = self.email_address
        external_reference = self.external_reference
        phone_number = self.phone_number
        qualifier = self.qualifier
        redirected_destination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.redirected_destination, Unset):
            redirected_destination = self.redirected_destination.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "customerId": customer_id,
                "defaultReference": default_reference,
                "destinationIdentifier": destination_identifier,
                "id": id,
                "name": name,
                "status": status,
                "updated": updated,
            }
        )
        if access_groups is not UNSET:
            field_dict["accessGroups"] = access_groups
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if address is not UNSET:
            field_dict["address"] = address
        if approval_request_id is not UNSET:
            field_dict["approvalRequestId"] = approval_request_id
        if approval_required is not UNSET:
            field_dict["approvalRequired"] = approval_required
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status
        if birthdate is not UNSET:
            field_dict["birthdate"] = birthdate
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if qualifier is not UNSET:
            field_dict["qualifier"] = qualifier
        if redirected_destination is not UNSET:
            field_dict["redirectedDestination"] = redirected_destination

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_address_response import AccountAddressResponse
        from ..models.account_identifier_response import AccountIdentifierResponse

        d = src_dict.copy()
        created = isoparse(d.pop("created"))

        customer_id = d.pop("customerId")

        default_reference = d.pop("defaultReference")

        destination_identifier = AccountIdentifierResponse.from_dict(
            d.pop("destinationIdentifier")
        )

        id = d.pop("id")

        name = d.pop("name")

        status = d.pop("status")

        updated = isoparse(d.pop("updated"))

        access_groups = cast(List[str], d.pop("accessGroups", UNSET))

        account_id = d.pop("accountId", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, AccountAddressResponse]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = AccountAddressResponse.from_dict(_address)

        approval_request_id = d.pop("approvalRequestId", UNSET)

        approval_required = d.pop("approvalRequired", UNSET)

        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, AccountBeneficiaryResponseApprovalStatus]
        if isinstance(_approval_status, Unset):
            approval_status = UNSET
        else:
            approval_status = AccountBeneficiaryResponseApprovalStatus(_approval_status)

        _birthdate = d.pop("birthdate", UNSET)
        birthdate: Union[Unset, datetime.date]
        if isinstance(_birthdate, Unset):
            birthdate = UNSET
        else:
            birthdate = isoparse(_birthdate).date()

        email_address = d.pop("emailAddress", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        phone_number = d.pop("phoneNumber", UNSET)

        qualifier = d.pop("qualifier", UNSET)

        _redirected_destination = d.pop("redirectedDestination", UNSET)
        redirected_destination: Union[Unset, AccountIdentifierResponse]
        if isinstance(_redirected_destination, Unset):
            redirected_destination = UNSET
        else:
            redirected_destination = AccountIdentifierResponse.from_dict(_redirected_destination)

        account_beneficiary_response = cls(
            created=created,
            customer_id=customer_id,
            default_reference=default_reference,
            destination_identifier=destination_identifier,
            id=id,
            name=name,
            status=status,
            updated=updated,
            access_groups=access_groups,
            account_id=account_id,
            address=address,
            approval_request_id=approval_request_id,
            approval_required=approval_required,
            approval_status=approval_status,
            birthdate=birthdate,
            email_address=email_address,
            external_reference=external_reference,
            phone_number=phone_number,
            qualifier=qualifier,
            redirected_destination=redirected_destination,
        )

        account_beneficiary_response.additional_properties = d
        return account_beneficiary_response

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
