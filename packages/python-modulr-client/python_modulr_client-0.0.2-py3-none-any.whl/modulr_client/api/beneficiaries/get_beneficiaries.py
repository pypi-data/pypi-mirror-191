from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_beneficiary_page_response import AccountBeneficiaryPageResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    customer_id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    iban: Union[Unset, None, str] = UNSET,
    qualifier: Union[Unset, None, str] = UNSET,
    state: Union[Unset, None, str] = UNSET,
    created_date: Union[Unset, None, str] = UNSET,
    partial_name: Union[Unset, None, str] = UNSET,
    sort_code: Union[Unset, None, str] = UNSET,
    account_number: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/beneficiaries"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["id"] = id

    params["customerId"] = customer_id

    params["q"] = q

    params["modifiedSince"] = modified_since

    params["hasExternalReference"] = has_external_reference

    params["externalReference"] = external_reference

    params["iban"] = iban

    params["qualifier"] = qualifier

    params["state"] = state

    params["createdDate"] = created_date

    params["partialName"] = partial_name

    params["sortCode"] = sort_code

    params["accountNumber"] = account_number

    params["page"] = page

    params["size"] = size

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
) -> Optional[AccountBeneficiaryPageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountBeneficiaryPageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[AccountBeneficiaryPageResponse]:
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
    customer_id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    iban: Union[Unset, None, str] = UNSET,
    qualifier: Union[Unset, None, str] = UNSET,
    state: Union[Unset, None, str] = UNSET,
    created_date: Union[Unset, None, str] = UNSET,
    partial_name: Union[Unset, None, str] = UNSET,
    sort_code: Union[Unset, None, str] = UNSET,
    account_number: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
) -> Response[AccountBeneficiaryPageResponse]:
    """Retrieve beneficiaries

     The ability to get the details of beneficiaries using various pieces of information, e.g. using
    customer ID, retrieve all beneficiaries created by that customer. Can get details of one particular
    beneficiary based on the unique beneficiary reference number.

    Args:
        id (Union[Unset, None, str]): Id of Beneficiary(s) to fetch
        customer_id (Union[Unset, None, str]): Filter by Customer Id
        q (Union[Unset, None, str]): Partial name of beneficiary or Scan Details Or IBAN Or
            external reference Or default reference to search for
        modified_since (Union[Unset, None, str]): Beneficiaries modified after this date time
        has_external_reference (Union[Unset, None, bool]): Filter by existence of external
            reference
        external_reference (Union[Unset, None, str]): External reference for beneficiary
        iban (Union[Unset, None, str]): IBAN
        qualifier (Union[Unset, None, str]): A list of external qualifiers
        state (Union[Unset, None, str]): Approval item state(s) to filter by
        created_date (Union[Unset, None, str]): Created date
        partial_name (Union[Unset, None, str]): Partial name
        sort_code (Union[Unset, None, str]): Sort code
        account_number (Union[Unset, None, str]): Account number
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountBeneficiaryPageResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        customer_id=customer_id,
        q=q,
        modified_since=modified_since,
        has_external_reference=has_external_reference,
        external_reference=external_reference,
        iban=iban,
        qualifier=qualifier,
        state=state,
        created_date=created_date,
        partial_name=partial_name,
        sort_code=sort_code,
        account_number=account_number,
        page=page,
        size=size,
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
    customer_id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    iban: Union[Unset, None, str] = UNSET,
    qualifier: Union[Unset, None, str] = UNSET,
    state: Union[Unset, None, str] = UNSET,
    created_date: Union[Unset, None, str] = UNSET,
    partial_name: Union[Unset, None, str] = UNSET,
    sort_code: Union[Unset, None, str] = UNSET,
    account_number: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
) -> Optional[AccountBeneficiaryPageResponse]:
    """Retrieve beneficiaries

     The ability to get the details of beneficiaries using various pieces of information, e.g. using
    customer ID, retrieve all beneficiaries created by that customer. Can get details of one particular
    beneficiary based on the unique beneficiary reference number.

    Args:
        id (Union[Unset, None, str]): Id of Beneficiary(s) to fetch
        customer_id (Union[Unset, None, str]): Filter by Customer Id
        q (Union[Unset, None, str]): Partial name of beneficiary or Scan Details Or IBAN Or
            external reference Or default reference to search for
        modified_since (Union[Unset, None, str]): Beneficiaries modified after this date time
        has_external_reference (Union[Unset, None, bool]): Filter by existence of external
            reference
        external_reference (Union[Unset, None, str]): External reference for beneficiary
        iban (Union[Unset, None, str]): IBAN
        qualifier (Union[Unset, None, str]): A list of external qualifiers
        state (Union[Unset, None, str]): Approval item state(s) to filter by
        created_date (Union[Unset, None, str]): Created date
        partial_name (Union[Unset, None, str]): Partial name
        sort_code (Union[Unset, None, str]): Sort code
        account_number (Union[Unset, None, str]): Account number
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountBeneficiaryPageResponse]
    """

    return sync_detailed(
        client=client,
        id=id,
        customer_id=customer_id,
        q=q,
        modified_since=modified_since,
        has_external_reference=has_external_reference,
        external_reference=external_reference,
        iban=iban,
        qualifier=qualifier,
        state=state,
        created_date=created_date,
        partial_name=partial_name,
        sort_code=sort_code,
        account_number=account_number,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    customer_id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    iban: Union[Unset, None, str] = UNSET,
    qualifier: Union[Unset, None, str] = UNSET,
    state: Union[Unset, None, str] = UNSET,
    created_date: Union[Unset, None, str] = UNSET,
    partial_name: Union[Unset, None, str] = UNSET,
    sort_code: Union[Unset, None, str] = UNSET,
    account_number: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
) -> Response[AccountBeneficiaryPageResponse]:
    """Retrieve beneficiaries

     The ability to get the details of beneficiaries using various pieces of information, e.g. using
    customer ID, retrieve all beneficiaries created by that customer. Can get details of one particular
    beneficiary based on the unique beneficiary reference number.

    Args:
        id (Union[Unset, None, str]): Id of Beneficiary(s) to fetch
        customer_id (Union[Unset, None, str]): Filter by Customer Id
        q (Union[Unset, None, str]): Partial name of beneficiary or Scan Details Or IBAN Or
            external reference Or default reference to search for
        modified_since (Union[Unset, None, str]): Beneficiaries modified after this date time
        has_external_reference (Union[Unset, None, bool]): Filter by existence of external
            reference
        external_reference (Union[Unset, None, str]): External reference for beneficiary
        iban (Union[Unset, None, str]): IBAN
        qualifier (Union[Unset, None, str]): A list of external qualifiers
        state (Union[Unset, None, str]): Approval item state(s) to filter by
        created_date (Union[Unset, None, str]): Created date
        partial_name (Union[Unset, None, str]): Partial name
        sort_code (Union[Unset, None, str]): Sort code
        account_number (Union[Unset, None, str]): Account number
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountBeneficiaryPageResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        customer_id=customer_id,
        q=q,
        modified_since=modified_since,
        has_external_reference=has_external_reference,
        external_reference=external_reference,
        iban=iban,
        qualifier=qualifier,
        state=state,
        created_date=created_date,
        partial_name=partial_name,
        sort_code=sort_code,
        account_number=account_number,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    customer_id: Union[Unset, None, str] = UNSET,
    q: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    iban: Union[Unset, None, str] = UNSET,
    qualifier: Union[Unset, None, str] = UNSET,
    state: Union[Unset, None, str] = UNSET,
    created_date: Union[Unset, None, str] = UNSET,
    partial_name: Union[Unset, None, str] = UNSET,
    sort_code: Union[Unset, None, str] = UNSET,
    account_number: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
) -> Optional[AccountBeneficiaryPageResponse]:
    """Retrieve beneficiaries

     The ability to get the details of beneficiaries using various pieces of information, e.g. using
    customer ID, retrieve all beneficiaries created by that customer. Can get details of one particular
    beneficiary based on the unique beneficiary reference number.

    Args:
        id (Union[Unset, None, str]): Id of Beneficiary(s) to fetch
        customer_id (Union[Unset, None, str]): Filter by Customer Id
        q (Union[Unset, None, str]): Partial name of beneficiary or Scan Details Or IBAN Or
            external reference Or default reference to search for
        modified_since (Union[Unset, None, str]): Beneficiaries modified after this date time
        has_external_reference (Union[Unset, None, bool]): Filter by existence of external
            reference
        external_reference (Union[Unset, None, str]): External reference for beneficiary
        iban (Union[Unset, None, str]): IBAN
        qualifier (Union[Unset, None, str]): A list of external qualifiers
        state (Union[Unset, None, str]): Approval item state(s) to filter by
        created_date (Union[Unset, None, str]): Created date
        partial_name (Union[Unset, None, str]): Partial name
        sort_code (Union[Unset, None, str]): Sort code
        account_number (Union[Unset, None, str]): Account number
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountBeneficiaryPageResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            customer_id=customer_id,
            q=q,
            modified_since=modified_since,
            has_external_reference=has_external_reference,
            external_reference=external_reference,
            iban=iban,
            qualifier=qualifier,
            state=state,
            created_date=created_date,
            partial_name=partial_name,
            sort_code=sort_code,
            account_number=account_number,
            page=page,
            size=size,
        )
    ).parsed
