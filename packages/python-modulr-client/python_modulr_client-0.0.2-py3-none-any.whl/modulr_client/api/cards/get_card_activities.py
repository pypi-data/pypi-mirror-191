from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.card_card_page_response_card_activity_response import (
    CardCardPageResponseCardActivityResponse,
)
from ...models.get_card_activities_statuses import GetCardActivitiesStatuses
from ...models.get_card_activities_types import GetCardActivitiesTypes
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardActivitiesStatuses] = UNSET,
    types: Union[Unset, None, GetCardActivitiesTypes] = UNSET,
    cards: Union[Unset, None, List[str]] = UNSET,
    accounts: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, List[str]] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Dict[str, Any]:
    url = f"{client.base_url}/activities"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["fromCreatedDate"] = from_created_date

    params["toCreatedDate"] = to_created_date

    json_statuses: Union[Unset, None, str] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = statuses.value if statuses else None

    params["statuses"] = json_statuses

    json_types: Union[Unset, None, str] = UNSET
    if not isinstance(types, Unset):
        json_types = types.value if types else None

    params["types"] = json_types

    json_cards: Union[Unset, None, List[str]] = UNSET
    if not isinstance(cards, Unset):
        if cards is None:
            json_cards = None
        else:
            json_cards = cards

    params["cards"] = json_cards

    json_accounts: Union[Unset, None, List[str]] = UNSET
    if not isinstance(accounts, Unset):
        if accounts is None:
            json_accounts = None
        else:
            json_accounts = accounts

    params["accounts"] = json_accounts

    json_ids: Union[Unset, None, List[str]] = UNSET
    if not isinstance(ids, Unset):
        if ids is None:
            json_ids = None
        else:
            json_ids = ids

    params["ids"] = json_ids

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
) -> Optional[CardCardPageResponseCardActivityResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CardCardPageResponseCardActivityResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardCardPageResponseCardActivityResponse]:
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
    statuses: Union[Unset, None, GetCardActivitiesStatuses] = UNSET,
    types: Union[Unset, None, GetCardActivitiesTypes] = UNSET,
    cards: Union[Unset, None, List[str]] = UNSET,
    accounts: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, List[str]] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[CardCardPageResponseCardActivityResponse]:
    """View activities for specific cards or over a date range

     View activities for a specified list of cards and a given time frame. View activities for all cards
    belonging to a specified list of accounts and a given time frame. View all activities for a single
    card when a single card ID is specified, time frame is optional.

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardActivitiesStatuses]):
        types (Union[Unset, None, GetCardActivitiesTypes]):
        cards (Union[Unset, None, List[str]]):
        accounts (Union[Unset, None, List[str]]):
        ids (Union[Unset, None, List[str]]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardActivityResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        statuses=statuses,
        types=types,
        cards=cards,
        accounts=accounts,
        ids=ids,
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
    statuses: Union[Unset, None, GetCardActivitiesStatuses] = UNSET,
    types: Union[Unset, None, GetCardActivitiesTypes] = UNSET,
    cards: Union[Unset, None, List[str]] = UNSET,
    accounts: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, List[str]] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Optional[CardCardPageResponseCardActivityResponse]:
    """View activities for specific cards or over a date range

     View activities for a specified list of cards and a given time frame. View activities for all cards
    belonging to a specified list of accounts and a given time frame. View all activities for a single
    card when a single card ID is specified, time frame is optional.

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardActivitiesStatuses]):
        types (Union[Unset, None, GetCardActivitiesTypes]):
        cards (Union[Unset, None, List[str]]):
        accounts (Union[Unset, None, List[str]]):
        ids (Union[Unset, None, List[str]]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardActivityResponse]
    """

    return sync_detailed(
        client=client,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        statuses=statuses,
        types=types,
        cards=cards,
        accounts=accounts,
        ids=ids,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    statuses: Union[Unset, None, GetCardActivitiesStatuses] = UNSET,
    types: Union[Unset, None, GetCardActivitiesTypes] = UNSET,
    cards: Union[Unset, None, List[str]] = UNSET,
    accounts: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, List[str]] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[CardCardPageResponseCardActivityResponse]:
    """View activities for specific cards or over a date range

     View activities for a specified list of cards and a given time frame. View activities for all cards
    belonging to a specified list of accounts and a given time frame. View all activities for a single
    card when a single card ID is specified, time frame is optional.

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardActivitiesStatuses]):
        types (Union[Unset, None, GetCardActivitiesTypes]):
        cards (Union[Unset, None, List[str]]):
        accounts (Union[Unset, None, List[str]]):
        ids (Union[Unset, None, List[str]]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardActivityResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        statuses=statuses,
        types=types,
        cards=cards,
        accounts=accounts,
        ids=ids,
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
    statuses: Union[Unset, None, GetCardActivitiesStatuses] = UNSET,
    types: Union[Unset, None, GetCardActivitiesTypes] = UNSET,
    cards: Union[Unset, None, List[str]] = UNSET,
    accounts: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, List[str]] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Optional[CardCardPageResponseCardActivityResponse]:
    """View activities for specific cards or over a date range

     View activities for a specified list of cards and a given time frame. View activities for all cards
    belonging to a specified list of accounts and a given time frame. View all activities for a single
    card when a single card ID is specified, time frame is optional.

    Args:
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        statuses (Union[Unset, None, GetCardActivitiesStatuses]):
        types (Union[Unset, None, GetCardActivitiesTypes]):
        cards (Union[Unset, None, List[str]]):
        accounts (Union[Unset, None, List[str]]):
        ids (Union[Unset, None, List[str]]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPageResponseCardActivityResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_created_date=from_created_date,
            to_created_date=to_created_date,
            statuses=statuses,
            types=types,
            cards=cards,
            accounts=accounts,
            ids=ids,
            page=page,
            size=size,
        )
    ).parsed
