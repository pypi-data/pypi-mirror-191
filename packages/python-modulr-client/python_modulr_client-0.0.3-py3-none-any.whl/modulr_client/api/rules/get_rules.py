from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.rule_rule_page_response import RuleRulePageResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    account_id: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
    rtype: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = f"{client.base_url}/accounts/{account_id}/rules"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["size"] = size

    params["rtype"] = rtype

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[RuleRulePageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RuleRulePageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[RuleRulePageResponse]:
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
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
    rtype: Union[Unset, None, str] = "",
) -> Response[RuleRulePageResponse]:
    """Get all Rules for a specific Account

     The ability to get the details of all rules associated with the specified account using the Account
    ID as a reference. Can filter by a specific type using the type parameter.

    Args:
        account_id (str):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.
        rtype (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRulePageResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        client=client,
        page=page,
        size=size,
        rtype=rtype,
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
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
    rtype: Union[Unset, None, str] = "",
) -> Optional[RuleRulePageResponse]:
    """Get all Rules for a specific Account

     The ability to get the details of all rules associated with the specified account using the Account
    ID as a reference. Can filter by a specific type using the type parameter.

    Args:
        account_id (str):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.
        rtype (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRulePageResponse]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        page=page,
        size=size,
        rtype=rtype,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
    rtype: Union[Unset, None, str] = "",
) -> Response[RuleRulePageResponse]:
    """Get all Rules for a specific Account

     The ability to get the details of all rules associated with the specified account using the Account
    ID as a reference. Can filter by a specific type using the type parameter.

    Args:
        account_id (str):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.
        rtype (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRulePageResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        client=client,
        page=page,
        size=size,
        rtype=rtype,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
    rtype: Union[Unset, None, str] = "",
) -> Optional[RuleRulePageResponse]:
    """Get all Rules for a specific Account

     The ability to get the details of all rules associated with the specified account using the Account
    ID as a reference. Can filter by a specific type using the type parameter.

    Args:
        account_id (str):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.
        rtype (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRulePageResponse]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            page=page,
            size=size,
            rtype=rtype,
        )
    ).parsed
