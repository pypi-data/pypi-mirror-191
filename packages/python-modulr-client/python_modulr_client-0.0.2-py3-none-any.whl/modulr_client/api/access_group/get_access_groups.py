from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_access_group_response import AccountAccessGroupResponse
from ...models.get_access_groups_statuses_item import GetAccessGroupsStatusesItem
from ...models.get_access_groups_types_item import GetAccessGroupsTypesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    ids: Union[Unset, None, List[str]] = UNSET,
    types: Union[Unset, None, List[GetAccessGroupsTypesItem]] = UNSET,
    statuses: Union[Unset, None, List[GetAccessGroupsStatusesItem]] = UNSET,
    type_ids: Union[Unset, None, List[str]] = UNSET,
    show_count_of_accounts: Union[Unset, None, str] = "true",
) -> Dict[str, Any]:
    url = f"{client.base_url}/access-groups"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_ids: Union[Unset, None, List[str]] = UNSET
    if not isinstance(ids, Unset):
        if ids is None:
            json_ids = None
        else:
            json_ids = ids

    params["ids"] = json_ids

    json_types: Union[Unset, None, List[str]] = UNSET
    if not isinstance(types, Unset):
        if types is None:
            json_types = None
        else:
            json_types = []
            for types_item_data in types:
                types_item = types_item_data.value

                json_types.append(types_item)

    params["types"] = json_types

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

    json_type_ids: Union[Unset, None, List[str]] = UNSET
    if not isinstance(type_ids, Unset):
        if type_ids is None:
            json_type_ids = None
        else:
            json_type_ids = type_ids

    params["typeIds"] = json_type_ids

    params["showCountOfAccounts"] = show_count_of_accounts

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
) -> Optional[List["AccountAccessGroupResponse"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AccountAccessGroupResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[List["AccountAccessGroupResponse"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ids: Union[Unset, None, List[str]] = UNSET,
    types: Union[Unset, None, List[GetAccessGroupsTypesItem]] = UNSET,
    statuses: Union[Unset, None, List[GetAccessGroupsStatusesItem]] = UNSET,
    type_ids: Union[Unset, None, List[str]] = UNSET,
    show_count_of_accounts: Union[Unset, None, str] = "true",
) -> Response[List["AccountAccessGroupResponse"]]:
    """Get a list of access groups

     The ability to list all access groups for the customer

    Args:
        ids (Union[Unset, None, List[str]]): ID of access group(s) to fetch
        types (Union[Unset, None, List[GetAccessGroupsTypesItem]]): Access group types
        statuses (Union[Unset, None, List[GetAccessGroupsStatusesItem]]): Access group statuses
        type_ids (Union[Unset, None, List[str]]): Ids of the entity implied by the type(s), e.g.
            the partner ID
        show_count_of_accounts (Union[Unset, None, str]): Whether to include the count of accounts
            in the response Default: 'true'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['AccountAccessGroupResponse']]
    """

    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        types=types,
        statuses=statuses,
        type_ids=type_ids,
        show_count_of_accounts=show_count_of_accounts,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    ids: Union[Unset, None, List[str]] = UNSET,
    types: Union[Unset, None, List[GetAccessGroupsTypesItem]] = UNSET,
    statuses: Union[Unset, None, List[GetAccessGroupsStatusesItem]] = UNSET,
    type_ids: Union[Unset, None, List[str]] = UNSET,
    show_count_of_accounts: Union[Unset, None, str] = "true",
) -> Optional[List["AccountAccessGroupResponse"]]:
    """Get a list of access groups

     The ability to list all access groups for the customer

    Args:
        ids (Union[Unset, None, List[str]]): ID of access group(s) to fetch
        types (Union[Unset, None, List[GetAccessGroupsTypesItem]]): Access group types
        statuses (Union[Unset, None, List[GetAccessGroupsStatusesItem]]): Access group statuses
        type_ids (Union[Unset, None, List[str]]): Ids of the entity implied by the type(s), e.g.
            the partner ID
        show_count_of_accounts (Union[Unset, None, str]): Whether to include the count of accounts
            in the response Default: 'true'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['AccountAccessGroupResponse']]
    """

    return sync_detailed(
        client=client,
        ids=ids,
        types=types,
        statuses=statuses,
        type_ids=type_ids,
        show_count_of_accounts=show_count_of_accounts,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ids: Union[Unset, None, List[str]] = UNSET,
    types: Union[Unset, None, List[GetAccessGroupsTypesItem]] = UNSET,
    statuses: Union[Unset, None, List[GetAccessGroupsStatusesItem]] = UNSET,
    type_ids: Union[Unset, None, List[str]] = UNSET,
    show_count_of_accounts: Union[Unset, None, str] = "true",
) -> Response[List["AccountAccessGroupResponse"]]:
    """Get a list of access groups

     The ability to list all access groups for the customer

    Args:
        ids (Union[Unset, None, List[str]]): ID of access group(s) to fetch
        types (Union[Unset, None, List[GetAccessGroupsTypesItem]]): Access group types
        statuses (Union[Unset, None, List[GetAccessGroupsStatusesItem]]): Access group statuses
        type_ids (Union[Unset, None, List[str]]): Ids of the entity implied by the type(s), e.g.
            the partner ID
        show_count_of_accounts (Union[Unset, None, str]): Whether to include the count of accounts
            in the response Default: 'true'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['AccountAccessGroupResponse']]
    """

    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        types=types,
        statuses=statuses,
        type_ids=type_ids,
        show_count_of_accounts=show_count_of_accounts,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    ids: Union[Unset, None, List[str]] = UNSET,
    types: Union[Unset, None, List[GetAccessGroupsTypesItem]] = UNSET,
    statuses: Union[Unset, None, List[GetAccessGroupsStatusesItem]] = UNSET,
    type_ids: Union[Unset, None, List[str]] = UNSET,
    show_count_of_accounts: Union[Unset, None, str] = "true",
) -> Optional[List["AccountAccessGroupResponse"]]:
    """Get a list of access groups

     The ability to list all access groups for the customer

    Args:
        ids (Union[Unset, None, List[str]]): ID of access group(s) to fetch
        types (Union[Unset, None, List[GetAccessGroupsTypesItem]]): Access group types
        statuses (Union[Unset, None, List[GetAccessGroupsStatusesItem]]): Access group statuses
        type_ids (Union[Unset, None, List[str]]): Ids of the entity implied by the type(s), e.g.
            the partner ID
        show_count_of_accounts (Union[Unset, None, str]): Whether to include the count of accounts
            in the response Default: 'true'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['AccountAccessGroupResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            ids=ids,
            types=types,
            statuses=statuses,
            type_ids=type_ids,
            show_count_of_accounts=show_count_of_accounts,
        )
    ).parsed
