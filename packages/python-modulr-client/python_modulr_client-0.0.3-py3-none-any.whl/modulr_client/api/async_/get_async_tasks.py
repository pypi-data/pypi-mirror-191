from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.card_card_page_response_async_task_response import (
    CardCardPageResponseAsyncTaskResponse,
)
from ...models.get_async_tasks_statuses import GetAsyncTasksStatuses
from ...models.get_async_tasks_types import GetAsyncTasksTypes
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    aid: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetAsyncTasksStatuses] = UNSET,
    types: Union[Unset, None, GetAsyncTasksTypes] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Dict[str, Any]:
    url = f"{client.base_url}/card-tasks"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["id"] = id

    params["aid"] = aid

    json_statuses: Union[Unset, None, str] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = statuses.value if statuses else None

    params["statuses"] = json_statuses

    json_types: Union[Unset, None, str] = UNSET
    if not isinstance(types, Unset):
        json_types = types.value if types else None

    params["types"] = json_types

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
) -> Optional[CardCardPageResponseAsyncTaskResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CardCardPageResponseAsyncTaskResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardCardPageResponseAsyncTaskResponse]:
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
    aid: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetAsyncTasksStatuses] = UNSET,
    types: Union[Unset, None, GetAsyncTasksTypes] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[CardCardPageResponseAsyncTaskResponse]:
    """Get tasks

     View the details of card tasks.  Ordered by createdDate, with the newest entries appearing first

    Args:
        id (Union[Unset, None, str]):
        aid (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetAsyncTasksStatuses]):
        types (Union[Unset, None, GetAsyncTasksTypes]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseAsyncTaskResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        aid=aid,
        statuses=statuses,
        types=types,
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
    aid: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetAsyncTasksStatuses] = UNSET,
    types: Union[Unset, None, GetAsyncTasksTypes] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Optional[CardCardPageResponseAsyncTaskResponse]:
    """Get tasks

     View the details of card tasks.  Ordered by createdDate, with the newest entries appearing first

    Args:
        id (Union[Unset, None, str]):
        aid (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetAsyncTasksStatuses]):
        types (Union[Unset, None, GetAsyncTasksTypes]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseAsyncTaskResponse]
    """

    return sync_detailed(
        client=client,
        id=id,
        aid=aid,
        statuses=statuses,
        types=types,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    aid: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetAsyncTasksStatuses] = UNSET,
    types: Union[Unset, None, GetAsyncTasksTypes] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[CardCardPageResponseAsyncTaskResponse]:
    """Get tasks

     View the details of card tasks.  Ordered by createdDate, with the newest entries appearing first

    Args:
        id (Union[Unset, None, str]):
        aid (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetAsyncTasksStatuses]):
        types (Union[Unset, None, GetAsyncTasksTypes]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseAsyncTaskResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        aid=aid,
        statuses=statuses,
        types=types,
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
    aid: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetAsyncTasksStatuses] = UNSET,
    types: Union[Unset, None, GetAsyncTasksTypes] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Optional[CardCardPageResponseAsyncTaskResponse]:
    """Get tasks

     View the details of card tasks.  Ordered by createdDate, with the newest entries appearing first

    Args:
        id (Union[Unset, None, str]):
        aid (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetAsyncTasksStatuses]):
        types (Union[Unset, None, GetAsyncTasksTypes]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseAsyncTaskResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            aid=aid,
            statuses=statuses,
            types=types,
            page=page,
            size=size,
        )
    ).parsed
