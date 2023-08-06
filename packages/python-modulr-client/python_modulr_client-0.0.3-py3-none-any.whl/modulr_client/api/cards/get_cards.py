from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.card_card_page_response_card_response import (
    CardCardPageResponseCardResponse,
)
from ...models.get_cards_statuses import GetCardsStatuses
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardsStatuses] = UNSET,
    id: Union[Unset, None, str] = UNSET,
    account_id: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Dict[str, Any]:
    url = f"{client.base_url}/cards"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["fromCreatedDate"] = from_created_date

    params["toCreatedDate"] = to_created_date

    json_statuses: Union[Unset, None, str] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = statuses.value if statuses else None

    params["statuses"] = json_statuses

    params["id"] = id

    params["accountId"] = account_id

    params["externalRef"] = external_ref

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
) -> Optional[CardCardPageResponseCardResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CardCardPageResponseCardResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardCardPageResponseCardResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardsStatuses] = UNSET,
    id: Union[Unset, None, str] = UNSET,
    account_id: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[CardCardPageResponseCardResponse]:
    """View the details of existing cards

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardsStatuses]):
        id (Union[Unset, None, str]):
        account_id (Union[Unset, None, str]):
        external_ref (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        statuses=statuses,
        id=id,
        account_id=account_id,
        external_ref=external_ref,
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
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardsStatuses] = UNSET,
    id: Union[Unset, None, str] = UNSET,
    account_id: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Optional[CardCardPageResponseCardResponse]:
    """View the details of existing cards

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardsStatuses]):
        id (Union[Unset, None, str]):
        account_id (Union[Unset, None, str]):
        external_ref (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardResponse]
    """

    return sync_detailed(
        client=client,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        statuses=statuses,
        id=id,
        account_id=account_id,
        external_ref=external_ref,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardsStatuses] = UNSET,
    id: Union[Unset, None, str] = UNSET,
    account_id: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[CardCardPageResponseCardResponse]:
    """View the details of existing cards

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardsStatuses]):
        id (Union[Unset, None, str]):
        account_id (Union[Unset, None, str]):
        external_ref (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        statuses=statuses,
        id=id,
        account_id=account_id,
        external_ref=external_ref,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardsStatuses] = UNSET,
    id: Union[Unset, None, str] = UNSET,
    account_id: Union[Unset, None, str] = UNSET,
    external_ref: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Optional[CardCardPageResponseCardResponse]:
    """View the details of existing cards

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardsStatuses]):
        id (Union[Unset, None, str]):
        account_id (Union[Unset, None, str]):
        external_ref (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_created_date=from_created_date,
            to_created_date=to_created_date,
            statuses=statuses,
            id=id,
            account_id=account_id,
            external_ref=external_ref,
            page=page,
            size=size,
        )
    ).parsed
