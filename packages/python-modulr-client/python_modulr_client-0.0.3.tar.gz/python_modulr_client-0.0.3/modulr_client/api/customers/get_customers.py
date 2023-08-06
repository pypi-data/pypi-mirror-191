import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_customer_page_response import AccountCustomerPageResponse
from ...models.account_string_search_criteria import AccountStringSearchCriteria
from ...models.get_customers_associate_search_criteria_associate_types_item import (
    GetCustomersAssociateSearchCriteriaAssociateTypesItem,
)
from ...models.get_customers_associate_search_criteria_last_name_type import (
    GetCustomersAssociateSearchCriteriaLastNameType,
)
from ...models.get_customers_name_type import GetCustomersNameType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    verification_status: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    name_type: GetCustomersNameType,
    name_value: str,
    company_reg_number: Union[Unset, None, str] = UNSET,
    legal_entity: Union[Unset, None, str] = UNSET,
    trading_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    trading_address_post_code: Union[Unset, None, str] = UNSET,
    trading_address_post_town: Union[Unset, None, str] = UNSET,
    trading_address_country: Union[Unset, None, str] = UNSET,
    trading_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    trading_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    registered_address_post_code: Union[Unset, None, str] = UNSET,
    registered_address_post_town: Union[Unset, None, str] = UNSET,
    registered_address_country: Union[Unset, None, str] = UNSET,
    registered_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_first_name_initial: Union[Unset, None, str] = UNSET,
    associate_search_criteria_last_name_type: GetCustomersAssociateSearchCriteriaLastNameType,
    associate_search_criteria_last_name_value: str,
    associate_search_criteria_last_names: Union[
        Unset, None, List["AccountStringSearchCriteria"]
    ] = UNSET,
    associate_search_criteria_last_name_prefix: Union[Unset, None, str] = UNSET,
    associate_search_criteria_date_of_birth: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_additional_identifier_type: str,
    associate_search_criteria_additional_identifier_value: str,
    associate_search_criteria_home_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    associate_search_criteria_home_address_post_code: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_post_town: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_country: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_home_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_associate_types: Union[
        Unset, None, List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]
    ] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["id"] = id

    params["q"] = q

    params["type"] = type

    params["verificationStatus"] = verification_status

    params["fromCreatedDate"] = from_created_date

    params["toCreatedDate"] = to_created_date

    params["page"] = page

    params["size"] = size

    params["sortField"] = sort_field

    params["sortOrder"] = sort_order

    params["externalRef"] = external_ref

    params["externalReference"] = external_reference

    json_name_type = name_type.value

    params["name.type"] = json_name_type

    params["name.value"] = name_value

    params["companyRegNumber"] = company_reg_number

    params["legalEntity"] = legal_entity

    json_trading_address_address_lines: Union[Unset, None, List[str]] = UNSET
    if not isinstance(trading_address_address_lines, Unset):
        if trading_address_address_lines is None:
            json_trading_address_address_lines = None
        else:
            json_trading_address_address_lines = trading_address_address_lines

    params["tradingAddress.addressLines"] = json_trading_address_address_lines

    params["tradingAddress.postCode"] = trading_address_post_code

    params["tradingAddress.postTown"] = trading_address_post_town

    params["tradingAddress.country"] = trading_address_country

    json_trading_address_start_date: Union[Unset, None, str] = UNSET
    if not isinstance(trading_address_start_date, Unset):
        json_trading_address_start_date = (
            trading_address_start_date.isoformat() if trading_address_start_date else None
        )

    params["tradingAddress.startDate"] = json_trading_address_start_date

    json_trading_address_end_date: Union[Unset, None, str] = UNSET
    if not isinstance(trading_address_end_date, Unset):
        json_trading_address_end_date = (
            trading_address_end_date.isoformat() if trading_address_end_date else None
        )

    params["tradingAddress.endDate"] = json_trading_address_end_date

    json_registered_address_address_lines: Union[Unset, None, List[str]] = UNSET
    if not isinstance(registered_address_address_lines, Unset):
        if registered_address_address_lines is None:
            json_registered_address_address_lines = None
        else:
            json_registered_address_address_lines = registered_address_address_lines

    params["registeredAddress.addressLines"] = json_registered_address_address_lines

    params["registeredAddress.postCode"] = registered_address_post_code

    params["registeredAddress.postTown"] = registered_address_post_town

    params["registeredAddress.country"] = registered_address_country

    json_registered_address_start_date: Union[Unset, None, str] = UNSET
    if not isinstance(registered_address_start_date, Unset):
        json_registered_address_start_date = (
            registered_address_start_date.isoformat() if registered_address_start_date else None
        )

    params["registeredAddress.startDate"] = json_registered_address_start_date

    json_registered_address_end_date: Union[Unset, None, str] = UNSET
    if not isinstance(registered_address_end_date, Unset):
        json_registered_address_end_date = (
            registered_address_end_date.isoformat() if registered_address_end_date else None
        )

    params["registeredAddress.endDate"] = json_registered_address_end_date

    params[
        "associateSearchCriteria.firstNameInitial"
    ] = associate_search_criteria_first_name_initial

    json_associate_search_criteria_last_name_type = associate_search_criteria_last_name_type.value

    params["associateSearchCriteria.lastName.type"] = json_associate_search_criteria_last_name_type

    params["associateSearchCriteria.lastName.value"] = associate_search_criteria_last_name_value

    json_associate_search_criteria_last_names: Union[Unset, None, List[Dict[str, Any]]] = UNSET
    if not isinstance(associate_search_criteria_last_names, Unset):
        if associate_search_criteria_last_names is None:
            json_associate_search_criteria_last_names = None
        else:
            json_associate_search_criteria_last_names = []
            for (
                associate_search_criteria_last_names_item_data
            ) in associate_search_criteria_last_names:
                associate_search_criteria_last_names_item = (
                    associate_search_criteria_last_names_item_data.to_dict()
                )

                json_associate_search_criteria_last_names.append(
                    associate_search_criteria_last_names_item
                )

    params["associateSearchCriteria.lastNames"] = json_associate_search_criteria_last_names

    params["associateSearchCriteria.lastNamePrefix"] = associate_search_criteria_last_name_prefix

    json_associate_search_criteria_date_of_birth: Union[Unset, None, str] = UNSET
    if not isinstance(associate_search_criteria_date_of_birth, Unset):
        json_associate_search_criteria_date_of_birth = (
            associate_search_criteria_date_of_birth.isoformat()
            if associate_search_criteria_date_of_birth
            else None
        )

    params["associateSearchCriteria.dateOfBirth"] = json_associate_search_criteria_date_of_birth

    params[
        "associateSearchCriteria.additionalIdentifier.type"
    ] = associate_search_criteria_additional_identifier_type

    params[
        "associateSearchCriteria.additionalIdentifier.value"
    ] = associate_search_criteria_additional_identifier_value

    json_associate_search_criteria_home_address_address_lines: Union[
        Unset, None, List[str]
    ] = UNSET
    if not isinstance(associate_search_criteria_home_address_address_lines, Unset):
        if associate_search_criteria_home_address_address_lines is None:
            json_associate_search_criteria_home_address_address_lines = None
        else:
            json_associate_search_criteria_home_address_address_lines = (
                associate_search_criteria_home_address_address_lines
            )

    params[
        "associateSearchCriteria.homeAddress.addressLines"
    ] = json_associate_search_criteria_home_address_address_lines

    params[
        "associateSearchCriteria.homeAddress.postCode"
    ] = associate_search_criteria_home_address_post_code

    params[
        "associateSearchCriteria.homeAddress.postTown"
    ] = associate_search_criteria_home_address_post_town

    params[
        "associateSearchCriteria.homeAddress.country"
    ] = associate_search_criteria_home_address_country

    json_associate_search_criteria_home_address_start_date: Union[Unset, None, str] = UNSET
    if not isinstance(associate_search_criteria_home_address_start_date, Unset):
        json_associate_search_criteria_home_address_start_date = (
            associate_search_criteria_home_address_start_date.isoformat()
            if associate_search_criteria_home_address_start_date
            else None
        )

    params[
        "associateSearchCriteria.homeAddress.startDate"
    ] = json_associate_search_criteria_home_address_start_date

    json_associate_search_criteria_home_address_end_date: Union[Unset, None, str] = UNSET
    if not isinstance(associate_search_criteria_home_address_end_date, Unset):
        json_associate_search_criteria_home_address_end_date = (
            associate_search_criteria_home_address_end_date.isoformat()
            if associate_search_criteria_home_address_end_date
            else None
        )

    params[
        "associateSearchCriteria.homeAddress.endDate"
    ] = json_associate_search_criteria_home_address_end_date

    json_associate_search_criteria_associate_types: Union[Unset, None, List[str]] = UNSET
    if not isinstance(associate_search_criteria_associate_types, Unset):
        if associate_search_criteria_associate_types is None:
            json_associate_search_criteria_associate_types = None
        else:
            json_associate_search_criteria_associate_types = []
            for (
                associate_search_criteria_associate_types_item_data
            ) in associate_search_criteria_associate_types:
                associate_search_criteria_associate_types_item = (
                    associate_search_criteria_associate_types_item_data.value
                )

                json_associate_search_criteria_associate_types.append(
                    associate_search_criteria_associate_types_item
                )

    params[
        "associateSearchCriteria.associateTypes"
    ] = json_associate_search_criteria_associate_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[AccountCustomerPageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountCustomerPageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[AccountCustomerPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    verification_status: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    name_type: GetCustomersNameType,
    name_value: str,
    company_reg_number: Union[Unset, None, str] = UNSET,
    legal_entity: Union[Unset, None, str] = UNSET,
    trading_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    trading_address_post_code: Union[Unset, None, str] = UNSET,
    trading_address_post_town: Union[Unset, None, str] = UNSET,
    trading_address_country: Union[Unset, None, str] = UNSET,
    trading_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    trading_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    registered_address_post_code: Union[Unset, None, str] = UNSET,
    registered_address_post_town: Union[Unset, None, str] = UNSET,
    registered_address_country: Union[Unset, None, str] = UNSET,
    registered_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_first_name_initial: Union[Unset, None, str] = UNSET,
    associate_search_criteria_last_name_type: GetCustomersAssociateSearchCriteriaLastNameType,
    associate_search_criteria_last_name_value: str,
    associate_search_criteria_last_names: Union[
        Unset, None, List["AccountStringSearchCriteria"]
    ] = UNSET,
    associate_search_criteria_last_name_prefix: Union[Unset, None, str] = UNSET,
    associate_search_criteria_date_of_birth: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_additional_identifier_type: str,
    associate_search_criteria_additional_identifier_value: str,
    associate_search_criteria_home_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    associate_search_criteria_home_address_post_code: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_post_town: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_country: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_home_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_associate_types: Union[
        Unset, None, List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]
    ] = UNSET,
) -> Response[AccountCustomerPageResponse]:
    """Retrieve customers using filters

     Either using unique references, such as customer ID, or filter parameters, such as verification
    status, get details of any customers found.

    Args:
        id (Union[Unset, None, str]): ID of Customer(s) to fetch
        q (Union[Unset, None, str]): Query parameter. ID, name or external reference of customer
            to search for
        type (Union[Unset, None, str]): Type to filter, can be one of:
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
        verification_status (Union[Unset, None, str]): Verification Status to filter, can be one
            of:
            1. UNVERIFIED -> no verification checks have been completed
            2. VERIFIED -> verification checks completed satisfactorily
            3. EXVERIFIED -> verification completed externally
            4. REFERRED -> verification is pending manual review
            5. DECLINED -> verification is complete with a negative result
            6. REVIEWED -> verification check has been reviewed
        from_created_date (Union[Unset, None, str]): Customers created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        to_created_date (Union[Unset, None, str]): Customers created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field. Sorted by createdDate if not present
        sort_order (Union[Unset, None, str]): Sorting order:
            1. asc -> ascendant
            2. desc -> descendant
        external_ref (Union[Unset, None, str]): A list of external references to filter
        external_reference (Union[Unset, None, str]): A list of external references to filter
            Example: externalReference[0].type.
        name_type (GetCustomersNameType):
        name_value (str):
        company_reg_number (Union[Unset, None, str]): Customer registration number
        legal_entity (Union[Unset, None, str]): Customer legal entity
        trading_address_address_lines (Union[Unset, None, List[str]]):
        trading_address_post_code (Union[Unset, None, str]):
        trading_address_post_town (Union[Unset, None, str]):
        trading_address_country (Union[Unset, None, str]):
        trading_address_start_date (Union[Unset, None, datetime.date]):
        trading_address_end_date (Union[Unset, None, datetime.date]):
        registered_address_address_lines (Union[Unset, None, List[str]]):
        registered_address_post_code (Union[Unset, None, str]):
        registered_address_post_town (Union[Unset, None, str]):
        registered_address_country (Union[Unset, None, str]):
        registered_address_start_date (Union[Unset, None, datetime.date]):
        registered_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_first_name_initial (Union[Unset, None, str]):
        associate_search_criteria_last_name_type
            (GetCustomersAssociateSearchCriteriaLastNameType):
        associate_search_criteria_last_name_value (str):
        associate_search_criteria_last_names (Union[Unset, None,
            List['AccountStringSearchCriteria']]):
        associate_search_criteria_last_name_prefix (Union[Unset, None, str]):
        associate_search_criteria_date_of_birth (Union[Unset, None, datetime.date]):
        associate_search_criteria_additional_identifier_type (str): Type of additional personal
            identifier
        associate_search_criteria_additional_identifier_value (str): Personal identifier value
        associate_search_criteria_home_address_address_lines (Union[Unset, None, List[str]]):
        associate_search_criteria_home_address_post_code (Union[Unset, None, str]):
        associate_search_criteria_home_address_post_town (Union[Unset, None, str]):
        associate_search_criteria_home_address_country (Union[Unset, None, str]):
        associate_search_criteria_home_address_start_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_home_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_associate_types (Union[Unset, None,
            List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomerPageResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        q=q,
        type=type,
        verification_status=verification_status,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
        external_ref=external_ref,
        external_reference=external_reference,
        name_type=name_type,
        name_value=name_value,
        company_reg_number=company_reg_number,
        legal_entity=legal_entity,
        trading_address_address_lines=trading_address_address_lines,
        trading_address_post_code=trading_address_post_code,
        trading_address_post_town=trading_address_post_town,
        trading_address_country=trading_address_country,
        trading_address_start_date=trading_address_start_date,
        trading_address_end_date=trading_address_end_date,
        registered_address_address_lines=registered_address_address_lines,
        registered_address_post_code=registered_address_post_code,
        registered_address_post_town=registered_address_post_town,
        registered_address_country=registered_address_country,
        registered_address_start_date=registered_address_start_date,
        registered_address_end_date=registered_address_end_date,
        associate_search_criteria_first_name_initial=associate_search_criteria_first_name_initial,
        associate_search_criteria_last_name_type=associate_search_criteria_last_name_type,
        associate_search_criteria_last_name_value=associate_search_criteria_last_name_value,
        associate_search_criteria_last_names=associate_search_criteria_last_names,
        associate_search_criteria_last_name_prefix=associate_search_criteria_last_name_prefix,
        associate_search_criteria_date_of_birth=associate_search_criteria_date_of_birth,
        associate_search_criteria_additional_identifier_type=associate_search_criteria_additional_identifier_type,
        associate_search_criteria_additional_identifier_value=associate_search_criteria_additional_identifier_value,
        associate_search_criteria_home_address_address_lines=associate_search_criteria_home_address_address_lines,
        associate_search_criteria_home_address_post_code=associate_search_criteria_home_address_post_code,
        associate_search_criteria_home_address_post_town=associate_search_criteria_home_address_post_town,
        associate_search_criteria_home_address_country=associate_search_criteria_home_address_country,
        associate_search_criteria_home_address_start_date=associate_search_criteria_home_address_start_date,
        associate_search_criteria_home_address_end_date=associate_search_criteria_home_address_end_date,
        associate_search_criteria_associate_types=associate_search_criteria_associate_types,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    verification_status: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    name_type: GetCustomersNameType,
    name_value: str,
    company_reg_number: Union[Unset, None, str] = UNSET,
    legal_entity: Union[Unset, None, str] = UNSET,
    trading_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    trading_address_post_code: Union[Unset, None, str] = UNSET,
    trading_address_post_town: Union[Unset, None, str] = UNSET,
    trading_address_country: Union[Unset, None, str] = UNSET,
    trading_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    trading_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    registered_address_post_code: Union[Unset, None, str] = UNSET,
    registered_address_post_town: Union[Unset, None, str] = UNSET,
    registered_address_country: Union[Unset, None, str] = UNSET,
    registered_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_first_name_initial: Union[Unset, None, str] = UNSET,
    associate_search_criteria_last_name_type: GetCustomersAssociateSearchCriteriaLastNameType,
    associate_search_criteria_last_name_value: str,
    associate_search_criteria_last_names: Union[
        Unset, None, List["AccountStringSearchCriteria"]
    ] = UNSET,
    associate_search_criteria_last_name_prefix: Union[Unset, None, str] = UNSET,
    associate_search_criteria_date_of_birth: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_additional_identifier_type: str,
    associate_search_criteria_additional_identifier_value: str,
    associate_search_criteria_home_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    associate_search_criteria_home_address_post_code: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_post_town: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_country: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_home_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_associate_types: Union[
        Unset, None, List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]
    ] = UNSET,
) -> Optional[AccountCustomerPageResponse]:
    """Retrieve customers using filters

     Either using unique references, such as customer ID, or filter parameters, such as verification
    status, get details of any customers found.

    Args:
        id (Union[Unset, None, str]): ID of Customer(s) to fetch
        q (Union[Unset, None, str]): Query parameter. ID, name or external reference of customer
            to search for
        type (Union[Unset, None, str]): Type to filter, can be one of:
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
        verification_status (Union[Unset, None, str]): Verification Status to filter, can be one
            of:
            1. UNVERIFIED -> no verification checks have been completed
            2. VERIFIED -> verification checks completed satisfactorily
            3. EXVERIFIED -> verification completed externally
            4. REFERRED -> verification is pending manual review
            5. DECLINED -> verification is complete with a negative result
            6. REVIEWED -> verification check has been reviewed
        from_created_date (Union[Unset, None, str]): Customers created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        to_created_date (Union[Unset, None, str]): Customers created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field. Sorted by createdDate if not present
        sort_order (Union[Unset, None, str]): Sorting order:
            1. asc -> ascendant
            2. desc -> descendant
        external_ref (Union[Unset, None, str]): A list of external references to filter
        external_reference (Union[Unset, None, str]): A list of external references to filter
            Example: externalReference[0].type.
        name_type (GetCustomersNameType):
        name_value (str):
        company_reg_number (Union[Unset, None, str]): Customer registration number
        legal_entity (Union[Unset, None, str]): Customer legal entity
        trading_address_address_lines (Union[Unset, None, List[str]]):
        trading_address_post_code (Union[Unset, None, str]):
        trading_address_post_town (Union[Unset, None, str]):
        trading_address_country (Union[Unset, None, str]):
        trading_address_start_date (Union[Unset, None, datetime.date]):
        trading_address_end_date (Union[Unset, None, datetime.date]):
        registered_address_address_lines (Union[Unset, None, List[str]]):
        registered_address_post_code (Union[Unset, None, str]):
        registered_address_post_town (Union[Unset, None, str]):
        registered_address_country (Union[Unset, None, str]):
        registered_address_start_date (Union[Unset, None, datetime.date]):
        registered_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_first_name_initial (Union[Unset, None, str]):
        associate_search_criteria_last_name_type
            (GetCustomersAssociateSearchCriteriaLastNameType):
        associate_search_criteria_last_name_value (str):
        associate_search_criteria_last_names (Union[Unset, None,
            List['AccountStringSearchCriteria']]):
        associate_search_criteria_last_name_prefix (Union[Unset, None, str]):
        associate_search_criteria_date_of_birth (Union[Unset, None, datetime.date]):
        associate_search_criteria_additional_identifier_type (str): Type of additional personal
            identifier
        associate_search_criteria_additional_identifier_value (str): Personal identifier value
        associate_search_criteria_home_address_address_lines (Union[Unset, None, List[str]]):
        associate_search_criteria_home_address_post_code (Union[Unset, None, str]):
        associate_search_criteria_home_address_post_town (Union[Unset, None, str]):
        associate_search_criteria_home_address_country (Union[Unset, None, str]):
        associate_search_criteria_home_address_start_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_home_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_associate_types (Union[Unset, None,
            List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomerPageResponse]
    """

    return sync_detailed(
        client=client,
        id=id,
        q=q,
        type=type,
        verification_status=verification_status,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
        external_ref=external_ref,
        external_reference=external_reference,
        name_type=name_type,
        name_value=name_value,
        company_reg_number=company_reg_number,
        legal_entity=legal_entity,
        trading_address_address_lines=trading_address_address_lines,
        trading_address_post_code=trading_address_post_code,
        trading_address_post_town=trading_address_post_town,
        trading_address_country=trading_address_country,
        trading_address_start_date=trading_address_start_date,
        trading_address_end_date=trading_address_end_date,
        registered_address_address_lines=registered_address_address_lines,
        registered_address_post_code=registered_address_post_code,
        registered_address_post_town=registered_address_post_town,
        registered_address_country=registered_address_country,
        registered_address_start_date=registered_address_start_date,
        registered_address_end_date=registered_address_end_date,
        associate_search_criteria_first_name_initial=associate_search_criteria_first_name_initial,
        associate_search_criteria_last_name_type=associate_search_criteria_last_name_type,
        associate_search_criteria_last_name_value=associate_search_criteria_last_name_value,
        associate_search_criteria_last_names=associate_search_criteria_last_names,
        associate_search_criteria_last_name_prefix=associate_search_criteria_last_name_prefix,
        associate_search_criteria_date_of_birth=associate_search_criteria_date_of_birth,
        associate_search_criteria_additional_identifier_type=associate_search_criteria_additional_identifier_type,
        associate_search_criteria_additional_identifier_value=associate_search_criteria_additional_identifier_value,
        associate_search_criteria_home_address_address_lines=associate_search_criteria_home_address_address_lines,
        associate_search_criteria_home_address_post_code=associate_search_criteria_home_address_post_code,
        associate_search_criteria_home_address_post_town=associate_search_criteria_home_address_post_town,
        associate_search_criteria_home_address_country=associate_search_criteria_home_address_country,
        associate_search_criteria_home_address_start_date=associate_search_criteria_home_address_start_date,
        associate_search_criteria_home_address_end_date=associate_search_criteria_home_address_end_date,
        associate_search_criteria_associate_types=associate_search_criteria_associate_types,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    verification_status: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    name_type: GetCustomersNameType,
    name_value: str,
    company_reg_number: Union[Unset, None, str] = UNSET,
    legal_entity: Union[Unset, None, str] = UNSET,
    trading_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    trading_address_post_code: Union[Unset, None, str] = UNSET,
    trading_address_post_town: Union[Unset, None, str] = UNSET,
    trading_address_country: Union[Unset, None, str] = UNSET,
    trading_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    trading_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    registered_address_post_code: Union[Unset, None, str] = UNSET,
    registered_address_post_town: Union[Unset, None, str] = UNSET,
    registered_address_country: Union[Unset, None, str] = UNSET,
    registered_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_first_name_initial: Union[Unset, None, str] = UNSET,
    associate_search_criteria_last_name_type: GetCustomersAssociateSearchCriteriaLastNameType,
    associate_search_criteria_last_name_value: str,
    associate_search_criteria_last_names: Union[
        Unset, None, List["AccountStringSearchCriteria"]
    ] = UNSET,
    associate_search_criteria_last_name_prefix: Union[Unset, None, str] = UNSET,
    associate_search_criteria_date_of_birth: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_additional_identifier_type: str,
    associate_search_criteria_additional_identifier_value: str,
    associate_search_criteria_home_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    associate_search_criteria_home_address_post_code: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_post_town: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_country: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_home_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_associate_types: Union[
        Unset, None, List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]
    ] = UNSET,
) -> Response[AccountCustomerPageResponse]:
    """Retrieve customers using filters

     Either using unique references, such as customer ID, or filter parameters, such as verification
    status, get details of any customers found.

    Args:
        id (Union[Unset, None, str]): ID of Customer(s) to fetch
        q (Union[Unset, None, str]): Query parameter. ID, name or external reference of customer
            to search for
        type (Union[Unset, None, str]): Type to filter, can be one of:
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
        verification_status (Union[Unset, None, str]): Verification Status to filter, can be one
            of:
            1. UNVERIFIED -> no verification checks have been completed
            2. VERIFIED -> verification checks completed satisfactorily
            3. EXVERIFIED -> verification completed externally
            4. REFERRED -> verification is pending manual review
            5. DECLINED -> verification is complete with a negative result
            6. REVIEWED -> verification check has been reviewed
        from_created_date (Union[Unset, None, str]): Customers created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        to_created_date (Union[Unset, None, str]): Customers created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field. Sorted by createdDate if not present
        sort_order (Union[Unset, None, str]): Sorting order:
            1. asc -> ascendant
            2. desc -> descendant
        external_ref (Union[Unset, None, str]): A list of external references to filter
        external_reference (Union[Unset, None, str]): A list of external references to filter
            Example: externalReference[0].type.
        name_type (GetCustomersNameType):
        name_value (str):
        company_reg_number (Union[Unset, None, str]): Customer registration number
        legal_entity (Union[Unset, None, str]): Customer legal entity
        trading_address_address_lines (Union[Unset, None, List[str]]):
        trading_address_post_code (Union[Unset, None, str]):
        trading_address_post_town (Union[Unset, None, str]):
        trading_address_country (Union[Unset, None, str]):
        trading_address_start_date (Union[Unset, None, datetime.date]):
        trading_address_end_date (Union[Unset, None, datetime.date]):
        registered_address_address_lines (Union[Unset, None, List[str]]):
        registered_address_post_code (Union[Unset, None, str]):
        registered_address_post_town (Union[Unset, None, str]):
        registered_address_country (Union[Unset, None, str]):
        registered_address_start_date (Union[Unset, None, datetime.date]):
        registered_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_first_name_initial (Union[Unset, None, str]):
        associate_search_criteria_last_name_type
            (GetCustomersAssociateSearchCriteriaLastNameType):
        associate_search_criteria_last_name_value (str):
        associate_search_criteria_last_names (Union[Unset, None,
            List['AccountStringSearchCriteria']]):
        associate_search_criteria_last_name_prefix (Union[Unset, None, str]):
        associate_search_criteria_date_of_birth (Union[Unset, None, datetime.date]):
        associate_search_criteria_additional_identifier_type (str): Type of additional personal
            identifier
        associate_search_criteria_additional_identifier_value (str): Personal identifier value
        associate_search_criteria_home_address_address_lines (Union[Unset, None, List[str]]):
        associate_search_criteria_home_address_post_code (Union[Unset, None, str]):
        associate_search_criteria_home_address_post_town (Union[Unset, None, str]):
        associate_search_criteria_home_address_country (Union[Unset, None, str]):
        associate_search_criteria_home_address_start_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_home_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_associate_types (Union[Unset, None,
            List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomerPageResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        q=q,
        type=type,
        verification_status=verification_status,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
        external_ref=external_ref,
        external_reference=external_reference,
        name_type=name_type,
        name_value=name_value,
        company_reg_number=company_reg_number,
        legal_entity=legal_entity,
        trading_address_address_lines=trading_address_address_lines,
        trading_address_post_code=trading_address_post_code,
        trading_address_post_town=trading_address_post_town,
        trading_address_country=trading_address_country,
        trading_address_start_date=trading_address_start_date,
        trading_address_end_date=trading_address_end_date,
        registered_address_address_lines=registered_address_address_lines,
        registered_address_post_code=registered_address_post_code,
        registered_address_post_town=registered_address_post_town,
        registered_address_country=registered_address_country,
        registered_address_start_date=registered_address_start_date,
        registered_address_end_date=registered_address_end_date,
        associate_search_criteria_first_name_initial=associate_search_criteria_first_name_initial,
        associate_search_criteria_last_name_type=associate_search_criteria_last_name_type,
        associate_search_criteria_last_name_value=associate_search_criteria_last_name_value,
        associate_search_criteria_last_names=associate_search_criteria_last_names,
        associate_search_criteria_last_name_prefix=associate_search_criteria_last_name_prefix,
        associate_search_criteria_date_of_birth=associate_search_criteria_date_of_birth,
        associate_search_criteria_additional_identifier_type=associate_search_criteria_additional_identifier_type,
        associate_search_criteria_additional_identifier_value=associate_search_criteria_additional_identifier_value,
        associate_search_criteria_home_address_address_lines=associate_search_criteria_home_address_address_lines,
        associate_search_criteria_home_address_post_code=associate_search_criteria_home_address_post_code,
        associate_search_criteria_home_address_post_town=associate_search_criteria_home_address_post_town,
        associate_search_criteria_home_address_country=associate_search_criteria_home_address_country,
        associate_search_criteria_home_address_start_date=associate_search_criteria_home_address_start_date,
        associate_search_criteria_home_address_end_date=associate_search_criteria_home_address_end_date,
        associate_search_criteria_associate_types=associate_search_criteria_associate_types,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    verification_status: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    name_type: GetCustomersNameType,
    name_value: str,
    company_reg_number: Union[Unset, None, str] = UNSET,
    legal_entity: Union[Unset, None, str] = UNSET,
    trading_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    trading_address_post_code: Union[Unset, None, str] = UNSET,
    trading_address_post_town: Union[Unset, None, str] = UNSET,
    trading_address_country: Union[Unset, None, str] = UNSET,
    trading_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    trading_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    registered_address_post_code: Union[Unset, None, str] = UNSET,
    registered_address_post_town: Union[Unset, None, str] = UNSET,
    registered_address_country: Union[Unset, None, str] = UNSET,
    registered_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    registered_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_first_name_initial: Union[Unset, None, str] = UNSET,
    associate_search_criteria_last_name_type: GetCustomersAssociateSearchCriteriaLastNameType,
    associate_search_criteria_last_name_value: str,
    associate_search_criteria_last_names: Union[
        Unset, None, List["AccountStringSearchCriteria"]
    ] = UNSET,
    associate_search_criteria_last_name_prefix: Union[Unset, None, str] = UNSET,
    associate_search_criteria_date_of_birth: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_additional_identifier_type: str,
    associate_search_criteria_additional_identifier_value: str,
    associate_search_criteria_home_address_address_lines: Union[Unset, None, List[str]] = UNSET,
    associate_search_criteria_home_address_post_code: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_post_town: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_country: Union[Unset, None, str] = UNSET,
    associate_search_criteria_home_address_start_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_home_address_end_date: Union[Unset, None, datetime.date] = UNSET,
    associate_search_criteria_associate_types: Union[
        Unset, None, List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]
    ] = UNSET,
) -> Optional[AccountCustomerPageResponse]:
    """Retrieve customers using filters

     Either using unique references, such as customer ID, or filter parameters, such as verification
    status, get details of any customers found.

    Args:
        id (Union[Unset, None, str]): ID of Customer(s) to fetch
        q (Union[Unset, None, str]): Query parameter. ID, name or external reference of customer
            to search for
        type (Union[Unset, None, str]): Type to filter, can be one of:
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
        verification_status (Union[Unset, None, str]): Verification Status to filter, can be one
            of:
            1. UNVERIFIED -> no verification checks have been completed
            2. VERIFIED -> verification checks completed satisfactorily
            3. EXVERIFIED -> verification completed externally
            4. REFERRED -> verification is pending manual review
            5. DECLINED -> verification is complete with a negative result
            6. REVIEWED -> verification check has been reviewed
        from_created_date (Union[Unset, None, str]): Customers created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        to_created_date (Union[Unset, None, str]): Customers created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field. Sorted by createdDate if not present
        sort_order (Union[Unset, None, str]): Sorting order:
            1. asc -> ascendant
            2. desc -> descendant
        external_ref (Union[Unset, None, str]): A list of external references to filter
        external_reference (Union[Unset, None, str]): A list of external references to filter
            Example: externalReference[0].type.
        name_type (GetCustomersNameType):
        name_value (str):
        company_reg_number (Union[Unset, None, str]): Customer registration number
        legal_entity (Union[Unset, None, str]): Customer legal entity
        trading_address_address_lines (Union[Unset, None, List[str]]):
        trading_address_post_code (Union[Unset, None, str]):
        trading_address_post_town (Union[Unset, None, str]):
        trading_address_country (Union[Unset, None, str]):
        trading_address_start_date (Union[Unset, None, datetime.date]):
        trading_address_end_date (Union[Unset, None, datetime.date]):
        registered_address_address_lines (Union[Unset, None, List[str]]):
        registered_address_post_code (Union[Unset, None, str]):
        registered_address_post_town (Union[Unset, None, str]):
        registered_address_country (Union[Unset, None, str]):
        registered_address_start_date (Union[Unset, None, datetime.date]):
        registered_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_first_name_initial (Union[Unset, None, str]):
        associate_search_criteria_last_name_type
            (GetCustomersAssociateSearchCriteriaLastNameType):
        associate_search_criteria_last_name_value (str):
        associate_search_criteria_last_names (Union[Unset, None,
            List['AccountStringSearchCriteria']]):
        associate_search_criteria_last_name_prefix (Union[Unset, None, str]):
        associate_search_criteria_date_of_birth (Union[Unset, None, datetime.date]):
        associate_search_criteria_additional_identifier_type (str): Type of additional personal
            identifier
        associate_search_criteria_additional_identifier_value (str): Personal identifier value
        associate_search_criteria_home_address_address_lines (Union[Unset, None, List[str]]):
        associate_search_criteria_home_address_post_code (Union[Unset, None, str]):
        associate_search_criteria_home_address_post_town (Union[Unset, None, str]):
        associate_search_criteria_home_address_country (Union[Unset, None, str]):
        associate_search_criteria_home_address_start_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_home_address_end_date (Union[Unset, None, datetime.date]):
        associate_search_criteria_associate_types (Union[Unset, None,
            List[GetCustomersAssociateSearchCriteriaAssociateTypesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomerPageResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            q=q,
            type=type,
            verification_status=verification_status,
            from_created_date=from_created_date,
            to_created_date=to_created_date,
            page=page,
            size=size,
            sort_field=sort_field,
            sort_order=sort_order,
            external_ref=external_ref,
            external_reference=external_reference,
            name_type=name_type,
            name_value=name_value,
            company_reg_number=company_reg_number,
            legal_entity=legal_entity,
            trading_address_address_lines=trading_address_address_lines,
            trading_address_post_code=trading_address_post_code,
            trading_address_post_town=trading_address_post_town,
            trading_address_country=trading_address_country,
            trading_address_start_date=trading_address_start_date,
            trading_address_end_date=trading_address_end_date,
            registered_address_address_lines=registered_address_address_lines,
            registered_address_post_code=registered_address_post_code,
            registered_address_post_town=registered_address_post_town,
            registered_address_country=registered_address_country,
            registered_address_start_date=registered_address_start_date,
            registered_address_end_date=registered_address_end_date,
            associate_search_criteria_first_name_initial=associate_search_criteria_first_name_initial,
            associate_search_criteria_last_name_type=associate_search_criteria_last_name_type,
            associate_search_criteria_last_name_value=associate_search_criteria_last_name_value,
            associate_search_criteria_last_names=associate_search_criteria_last_names,
            associate_search_criteria_last_name_prefix=associate_search_criteria_last_name_prefix,
            associate_search_criteria_date_of_birth=associate_search_criteria_date_of_birth,
            associate_search_criteria_additional_identifier_type=associate_search_criteria_additional_identifier_type,
            associate_search_criteria_additional_identifier_value=associate_search_criteria_additional_identifier_value,
            associate_search_criteria_home_address_address_lines=associate_search_criteria_home_address_address_lines,
            associate_search_criteria_home_address_post_code=associate_search_criteria_home_address_post_code,
            associate_search_criteria_home_address_post_town=associate_search_criteria_home_address_post_town,
            associate_search_criteria_home_address_country=associate_search_criteria_home_address_country,
            associate_search_criteria_home_address_start_date=associate_search_criteria_home_address_start_date,
            associate_search_criteria_home_address_end_date=associate_search_criteria_home_address_end_date,
            associate_search_criteria_associate_types=associate_search_criteria_associate_types,
        )
    ).parsed
