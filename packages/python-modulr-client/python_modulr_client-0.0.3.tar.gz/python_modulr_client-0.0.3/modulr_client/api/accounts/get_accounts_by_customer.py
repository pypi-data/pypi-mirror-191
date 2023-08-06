from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_account_page_response import AccountAccountPageResponse
from ...models.account_customer_statuses_item import AccountCustomerStatusesItem
from ...models.account_statuses_item import AccountStatusesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    customer_id: str,
    *,
    client: Client,
    customer_statuses: Union[Unset, None, List[AccountCustomerStatusesItem]] = UNSET,
    statuses: Union[Unset, None, List[AccountStatusesItem]] = UNSET,
    min_balance: Union[Unset, None, str] = UNSET,
    max_balance: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    currency: Union[Unset, None, str] = UNSET,
    show_available_balance: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers/{customer_id}/accounts"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_customer_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(customer_statuses, Unset):
        if customer_statuses is None:
            json_customer_statuses = None
        else:
            json_customer_statuses = []
            for componentsschemasaccount_customer_statuses_item_data in customer_statuses:
                componentsschemasaccount_customer_statuses_item = (
                    componentsschemasaccount_customer_statuses_item_data.value
                )

                json_customer_statuses.append(componentsschemasaccount_customer_statuses_item)

    params["customerStatuses"] = json_customer_statuses

    json_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        if statuses is None:
            json_statuses = None
        else:
            json_statuses = []
            for componentsschemasaccount_statuses_item_data in statuses:
                componentsschemasaccount_statuses_item = (
                    componentsschemasaccount_statuses_item_data.value
                )

                json_statuses.append(componentsschemasaccount_statuses_item)

    params["statuses"] = json_statuses

    params["minBalance"] = min_balance

    params["maxBalance"] = max_balance

    params["fromCreatedDate"] = from_created_date

    params["toCreatedDate"] = to_created_date

    params["page"] = page

    params["size"] = size

    params["sortField"] = sort_field

    params["sortOrder"] = sort_order

    params["currency"] = currency

    params["showAvailableBalance"] = show_available_balance

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
) -> Optional[AccountAccountPageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountAccountPageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[AccountAccountPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    customer_id: str,
    *,
    client: Client,
    customer_statuses: Union[Unset, None, List[AccountCustomerStatusesItem]] = UNSET,
    statuses: Union[Unset, None, List[AccountStatusesItem]] = UNSET,
    min_balance: Union[Unset, None, str] = UNSET,
    max_balance: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    currency: Union[Unset, None, str] = UNSET,
    show_available_balance: Union[Unset, None, str] = UNSET,
) -> Response[AccountAccountPageResponse]:
    """Get accounts by customer

     Get details of accounts belonging to a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        customer_statuses (Union[Unset, None, List[AccountCustomerStatusesItem]]):
        statuses (Union[Unset, None, List[AccountStatusesItem]]):
        min_balance (Union[Unset, None, str]): Accounts with balance equal or more than this
            amount
        max_balance (Union[Unset, None, str]): Accounts with balance equal or less than this
            amount
        from_created_date (Union[Unset, None, str]): Accounts created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Accounts created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field
        sort_order (Union[Unset, None, str]): Sorting order
        currency (Union[Unset, None, str]): The currency for getting account by currency. Expected
            ISO Standard currency name i.e. GBP, EUR etc Example: GBP.
        show_available_balance (Union[Unset, None, str]): Show available balance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountPageResponse]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        customer_statuses=customer_statuses,
        statuses=statuses,
        min_balance=min_balance,
        max_balance=max_balance,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
        currency=currency,
        show_available_balance=show_available_balance,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    customer_id: str,
    *,
    client: Client,
    customer_statuses: Union[Unset, None, List[AccountCustomerStatusesItem]] = UNSET,
    statuses: Union[Unset, None, List[AccountStatusesItem]] = UNSET,
    min_balance: Union[Unset, None, str] = UNSET,
    max_balance: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    currency: Union[Unset, None, str] = UNSET,
    show_available_balance: Union[Unset, None, str] = UNSET,
) -> Optional[AccountAccountPageResponse]:
    """Get accounts by customer

     Get details of accounts belonging to a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        customer_statuses (Union[Unset, None, List[AccountCustomerStatusesItem]]):
        statuses (Union[Unset, None, List[AccountStatusesItem]]):
        min_balance (Union[Unset, None, str]): Accounts with balance equal or more than this
            amount
        max_balance (Union[Unset, None, str]): Accounts with balance equal or less than this
            amount
        from_created_date (Union[Unset, None, str]): Accounts created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Accounts created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field
        sort_order (Union[Unset, None, str]): Sorting order
        currency (Union[Unset, None, str]): The currency for getting account by currency. Expected
            ISO Standard currency name i.e. GBP, EUR etc Example: GBP.
        show_available_balance (Union[Unset, None, str]): Show available balance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountPageResponse]
    """

    return sync_detailed(
        customer_id=customer_id,
        client=client,
        customer_statuses=customer_statuses,
        statuses=statuses,
        min_balance=min_balance,
        max_balance=max_balance,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
        currency=currency,
        show_available_balance=show_available_balance,
    ).parsed


async def asyncio_detailed(
    customer_id: str,
    *,
    client: Client,
    customer_statuses: Union[Unset, None, List[AccountCustomerStatusesItem]] = UNSET,
    statuses: Union[Unset, None, List[AccountStatusesItem]] = UNSET,
    min_balance: Union[Unset, None, str] = UNSET,
    max_balance: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    currency: Union[Unset, None, str] = UNSET,
    show_available_balance: Union[Unset, None, str] = UNSET,
) -> Response[AccountAccountPageResponse]:
    """Get accounts by customer

     Get details of accounts belonging to a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        customer_statuses (Union[Unset, None, List[AccountCustomerStatusesItem]]):
        statuses (Union[Unset, None, List[AccountStatusesItem]]):
        min_balance (Union[Unset, None, str]): Accounts with balance equal or more than this
            amount
        max_balance (Union[Unset, None, str]): Accounts with balance equal or less than this
            amount
        from_created_date (Union[Unset, None, str]): Accounts created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Accounts created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field
        sort_order (Union[Unset, None, str]): Sorting order
        currency (Union[Unset, None, str]): The currency for getting account by currency. Expected
            ISO Standard currency name i.e. GBP, EUR etc Example: GBP.
        show_available_balance (Union[Unset, None, str]): Show available balance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountPageResponse]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        customer_statuses=customer_statuses,
        statuses=statuses,
        min_balance=min_balance,
        max_balance=max_balance,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
        currency=currency,
        show_available_balance=show_available_balance,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    customer_id: str,
    *,
    client: Client,
    customer_statuses: Union[Unset, None, List[AccountCustomerStatusesItem]] = UNSET,
    statuses: Union[Unset, None, List[AccountStatusesItem]] = UNSET,
    min_balance: Union[Unset, None, str] = UNSET,
    max_balance: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    currency: Union[Unset, None, str] = UNSET,
    show_available_balance: Union[Unset, None, str] = UNSET,
) -> Optional[AccountAccountPageResponse]:
    """Get accounts by customer

     Get details of accounts belonging to a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        customer_statuses (Union[Unset, None, List[AccountCustomerStatusesItem]]):
        statuses (Union[Unset, None, List[AccountStatusesItem]]):
        min_balance (Union[Unset, None, str]): Accounts with balance equal or more than this
            amount
        max_balance (Union[Unset, None, str]): Accounts with balance equal or less than this
            amount
        from_created_date (Union[Unset, None, str]): Accounts created after and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Accounts created before and on this date.
            Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g 2017-01-28T01:01:01+0000
            Example: 2017-01-28T01:01:01+0000.
        page (Union[Unset, None, str]): Page to fetch (0 indexed)
        size (Union[Unset, None, str]): Size of Page to fetch
        sort_field (Union[Unset, None, str]): Sort by field
        sort_order (Union[Unset, None, str]): Sorting order
        currency (Union[Unset, None, str]): The currency for getting account by currency. Expected
            ISO Standard currency name i.e. GBP, EUR etc Example: GBP.
        show_available_balance (Union[Unset, None, str]): Show available balance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountPageResponse]
    """

    return (
        await asyncio_detailed(
            customer_id=customer_id,
            client=client,
            customer_statuses=customer_statuses,
            statuses=statuses,
            min_balance=min_balance,
            max_balance=max_balance,
            from_created_date=from_created_date,
            to_created_date=to_created_date,
            page=page,
            size=size,
            sort_field=sort_field,
            sort_order=sort_order,
            currency=currency,
            show_available_balance=show_available_balance,
        )
    ).parsed
