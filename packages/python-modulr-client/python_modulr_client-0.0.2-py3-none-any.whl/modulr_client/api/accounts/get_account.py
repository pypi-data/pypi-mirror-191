from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_account_response import AccountAccountResponse
from ...models.get_account_statuses_item import GetAccountStatusesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetAccountStatusesItem]] = UNSET,
    include_pending_transactions: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = f"{client.base_url}/accounts/{id}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        if statuses is None:
            json_statuses = None
        else:
            json_statuses = []
            for statuses_item_data in statuses:
                statuses_item = statuses_item_data.value

                json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

    params["includePendingTransactions"] = include_pending_transactions

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
) -> Optional[AccountAccountResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountAccountResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[AccountAccountResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetAccountStatusesItem]] = UNSET,
    include_pending_transactions: Union[Unset, None, bool] = False,
) -> Response[AccountAccountResponse]:
    """Get an account

     Retrieve details of a particular account using its ID as a reference

    Args:
        id (str):
        statuses (Union[Unset, None, List[GetAccountStatusesItem]]):
        include_pending_transactions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        statuses=statuses,
        include_pending_transactions=include_pending_transactions,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetAccountStatusesItem]] = UNSET,
    include_pending_transactions: Union[Unset, None, bool] = False,
) -> Optional[AccountAccountResponse]:
    """Get an account

     Retrieve details of a particular account using its ID as a reference

    Args:
        id (str):
        statuses (Union[Unset, None, List[GetAccountStatusesItem]]):
        include_pending_transactions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        statuses=statuses,
        include_pending_transactions=include_pending_transactions,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetAccountStatusesItem]] = UNSET,
    include_pending_transactions: Union[Unset, None, bool] = False,
) -> Response[AccountAccountResponse]:
    """Get an account

     Retrieve details of a particular account using its ID as a reference

    Args:
        id (str):
        statuses (Union[Unset, None, List[GetAccountStatusesItem]]):
        include_pending_transactions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        statuses=statuses,
        include_pending_transactions=include_pending_transactions,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetAccountStatusesItem]] = UNSET,
    include_pending_transactions: Union[Unset, None, bool] = False,
) -> Optional[AccountAccountResponse]:
    """Get an account

     Retrieve details of a particular account using its ID as a reference

    Args:
        id (str):
        statuses (Union[Unset, None, List[GetAccountStatusesItem]]):
        include_pending_transactions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            statuses=statuses,
            include_pending_transactions=include_pending_transactions,
        )
    ).parsed
