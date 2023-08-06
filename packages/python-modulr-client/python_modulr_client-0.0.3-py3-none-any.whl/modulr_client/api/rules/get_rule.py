from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.rule_rule_response import RuleRuleResponse
from ...types import Response


def _get_kwargs(
    account_id: str,
    rtype: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/accounts/{accountId}/rules/{rtype}".format(
        client.base_url, accountId=account_id, rtype=rtype
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[RuleRuleResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RuleRuleResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[RuleRuleResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    rtype: str,
    *,
    client: Client,
) -> Response[RuleRuleResponse]:
    """Retrieve a Rule by rule type on a specific account

     You need to know the unique reference of the account and the rule type you want to get to
    information on.

    Args:
        account_id (str):
        rtype (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        rtype=rtype,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    rtype: str,
    *,
    client: Client,
) -> Optional[RuleRuleResponse]:
    """Retrieve a Rule by rule type on a specific account

     You need to know the unique reference of the account and the rule type you want to get to
    information on.

    Args:
        account_id (str):
        rtype (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    return sync_detailed(
        account_id=account_id,
        rtype=rtype,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    rtype: str,
    *,
    client: Client,
) -> Response[RuleRuleResponse]:
    """Retrieve a Rule by rule type on a specific account

     You need to know the unique reference of the account and the rule type you want to get to
    information on.

    Args:
        account_id (str):
        rtype (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        rtype=rtype,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    rtype: str,
    *,
    client: Client,
) -> Optional[RuleRuleResponse]:
    """Retrieve a Rule by rule type on a specific account

     You need to know the unique reference of the account and the rule type you want to get to
    information on.

    Args:
        account_id (str):
        rtype (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            rtype=rtype,
            client=client,
        )
    ).parsed
