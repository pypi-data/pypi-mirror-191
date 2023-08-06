from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_transaction_page_response import AccountTransactionPageResponse
from ...models.get_transactions_by_account_type_item import (
    GetTransactionsByAccountTypeItem,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    account_id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
    min_amount: Union[Unset, None, str] = UNSET,
    max_amount: Union[Unset, None, str] = UNSET,
    from_posted_date: Union[Unset, None, str] = UNSET,
    to_posted_date: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, List[GetTransactionsByAccountTypeItem]] = UNSET,
    credit: Union[Unset, None, bool] = UNSET,
    source_id: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    from_transaction_date: Union[Unset, None, str] = UNSET,
    to_transaction_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/accounts/{account_id}/transactions"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["q"] = q

    params["minAmount"] = min_amount

    params["maxAmount"] = max_amount

    params["fromPostedDate"] = from_posted_date

    params["toPostedDate"] = to_posted_date

    json_type: Union[Unset, None, List[str]] = UNSET
    if not isinstance(type, Unset):
        if type is None:
            json_type = None
        else:
            json_type = []
            for type_item_data in type:
                type_item = type_item_data.value

                json_type.append(type_item)

    params["type"] = json_type

    params["credit"] = credit

    params["sourceId"] = source_id

    params["size"] = size

    params["fromTransactionDate"] = from_transaction_date

    params["toTransactionDate"] = to_transaction_date

    params["page"] = page

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
) -> Optional[AccountTransactionPageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountTransactionPageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[AccountTransactionPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
    min_amount: Union[Unset, None, str] = UNSET,
    max_amount: Union[Unset, None, str] = UNSET,
    from_posted_date: Union[Unset, None, str] = UNSET,
    to_posted_date: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, List[GetTransactionsByAccountTypeItem]] = UNSET,
    credit: Union[Unset, None, bool] = UNSET,
    source_id: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    from_transaction_date: Union[Unset, None, str] = UNSET,
    to_transaction_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Response[AccountTransactionPageResponse]:
    """Get transactions for a specific Account

     Retrieves the last 6 months of transactions (successful payments in & out) of an account, specified
    by a unique account reference.

    Args:
        account_id (str):
        q (Union[Unset, None, str]): Partial description text to search for
        min_amount (Union[Unset, None, str]): Transactions with amount equal or more than this
            amount
        max_amount (Union[Unset, None, str]): Transactions with amount equal or less than this
            amount
        from_posted_date (Union[Unset, None, str]): Transactions with posted date equal or after
            to this date
        to_posted_date (Union[Unset, None, str]): Transactions with posted date equal or before to
            this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        type (Union[Unset, None, List[GetTransactionsByAccountTypeItem]]): Transaction types
        credit (Union[Unset, None, bool]): If true only credit transactions will be returned, if
            false, only debit transactions will be returned
        source_id (Union[Unset, None, str]): Transactions with this sourceId
        size (Union[Unset, None, str]): Size of Page to fetch
        from_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal
            or after to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        to_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal or
            before to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTransactionPageResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        client=client,
        q=q,
        min_amount=min_amount,
        max_amount=max_amount,
        from_posted_date=from_posted_date,
        to_posted_date=to_posted_date,
        type=type,
        credit=credit,
        source_id=source_id,
        size=size,
        from_transaction_date=from_transaction_date,
        to_transaction_date=to_transaction_date,
        page=page,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
    min_amount: Union[Unset, None, str] = UNSET,
    max_amount: Union[Unset, None, str] = UNSET,
    from_posted_date: Union[Unset, None, str] = UNSET,
    to_posted_date: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, List[GetTransactionsByAccountTypeItem]] = UNSET,
    credit: Union[Unset, None, bool] = UNSET,
    source_id: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    from_transaction_date: Union[Unset, None, str] = UNSET,
    to_transaction_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Optional[AccountTransactionPageResponse]:
    """Get transactions for a specific Account

     Retrieves the last 6 months of transactions (successful payments in & out) of an account, specified
    by a unique account reference.

    Args:
        account_id (str):
        q (Union[Unset, None, str]): Partial description text to search for
        min_amount (Union[Unset, None, str]): Transactions with amount equal or more than this
            amount
        max_amount (Union[Unset, None, str]): Transactions with amount equal or less than this
            amount
        from_posted_date (Union[Unset, None, str]): Transactions with posted date equal or after
            to this date
        to_posted_date (Union[Unset, None, str]): Transactions with posted date equal or before to
            this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        type (Union[Unset, None, List[GetTransactionsByAccountTypeItem]]): Transaction types
        credit (Union[Unset, None, bool]): If true only credit transactions will be returned, if
            false, only debit transactions will be returned
        source_id (Union[Unset, None, str]): Transactions with this sourceId
        size (Union[Unset, None, str]): Size of Page to fetch
        from_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal
            or after to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        to_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal or
            before to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTransactionPageResponse]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        q=q,
        min_amount=min_amount,
        max_amount=max_amount,
        from_posted_date=from_posted_date,
        to_posted_date=to_posted_date,
        type=type,
        credit=credit,
        source_id=source_id,
        size=size,
        from_transaction_date=from_transaction_date,
        to_transaction_date=to_transaction_date,
        page=page,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
    min_amount: Union[Unset, None, str] = UNSET,
    max_amount: Union[Unset, None, str] = UNSET,
    from_posted_date: Union[Unset, None, str] = UNSET,
    to_posted_date: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, List[GetTransactionsByAccountTypeItem]] = UNSET,
    credit: Union[Unset, None, bool] = UNSET,
    source_id: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    from_transaction_date: Union[Unset, None, str] = UNSET,
    to_transaction_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Response[AccountTransactionPageResponse]:
    """Get transactions for a specific Account

     Retrieves the last 6 months of transactions (successful payments in & out) of an account, specified
    by a unique account reference.

    Args:
        account_id (str):
        q (Union[Unset, None, str]): Partial description text to search for
        min_amount (Union[Unset, None, str]): Transactions with amount equal or more than this
            amount
        max_amount (Union[Unset, None, str]): Transactions with amount equal or less than this
            amount
        from_posted_date (Union[Unset, None, str]): Transactions with posted date equal or after
            to this date
        to_posted_date (Union[Unset, None, str]): Transactions with posted date equal or before to
            this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        type (Union[Unset, None, List[GetTransactionsByAccountTypeItem]]): Transaction types
        credit (Union[Unset, None, bool]): If true only credit transactions will be returned, if
            false, only debit transactions will be returned
        source_id (Union[Unset, None, str]): Transactions with this sourceId
        size (Union[Unset, None, str]): Size of Page to fetch
        from_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal
            or after to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        to_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal or
            before to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTransactionPageResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        client=client,
        q=q,
        min_amount=min_amount,
        max_amount=max_amount,
        from_posted_date=from_posted_date,
        to_posted_date=to_posted_date,
        type=type,
        credit=credit,
        source_id=source_id,
        size=size,
        from_transaction_date=from_transaction_date,
        to_transaction_date=to_transaction_date,
        page=page,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
    min_amount: Union[Unset, None, str] = UNSET,
    max_amount: Union[Unset, None, str] = UNSET,
    from_posted_date: Union[Unset, None, str] = UNSET,
    to_posted_date: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, List[GetTransactionsByAccountTypeItem]] = UNSET,
    credit: Union[Unset, None, bool] = UNSET,
    source_id: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, str] = UNSET,
    from_transaction_date: Union[Unset, None, str] = UNSET,
    to_transaction_date: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Optional[AccountTransactionPageResponse]:
    """Get transactions for a specific Account

     Retrieves the last 6 months of transactions (successful payments in & out) of an account, specified
    by a unique account reference.

    Args:
        account_id (str):
        q (Union[Unset, None, str]): Partial description text to search for
        min_amount (Union[Unset, None, str]): Transactions with amount equal or more than this
            amount
        max_amount (Union[Unset, None, str]): Transactions with amount equal or less than this
            amount
        from_posted_date (Union[Unset, None, str]): Transactions with posted date equal or after
            to this date
        to_posted_date (Union[Unset, None, str]): Transactions with posted date equal or before to
            this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        type (Union[Unset, None, List[GetTransactionsByAccountTypeItem]]): Transaction types
        credit (Union[Unset, None, bool]): If true only credit transactions will be returned, if
            false, only debit transactions will be returned
        source_id (Union[Unset, None, str]): Transactions with this sourceId
        size (Union[Unset, None, str]): Size of Page to fetch
        from_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal
            or after to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        to_transaction_date (Union[Unset, None, str]): Transactions with transaction date equal or
            before to this date. Format is 'yyyy-MM-dd'T'HH:mm:ssZ' where Z is UTC offset. e.g
            2017-01-28T01:01:01+0000
        page (Union[Unset, None, str]): Page to fetch (0 indexed)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountTransactionPageResponse]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            q=q,
            min_amount=min_amount,
            max_amount=max_amount,
            from_posted_date=from_posted_date,
            to_posted_date=to_posted_date,
            type=type,
            credit=credit,
            source_id=source_id,
            size=size,
            from_transaction_date=from_transaction_date,
            to_transaction_date=to_transaction_date,
            page=page,
        )
    ).parsed
