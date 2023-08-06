from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.rule_create_rule_request import RuleCreateRuleRequest
from ...models.rule_rule_response import RuleRuleResponse
from ...types import Response


def _get_kwargs(
    rule_id: str,
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/rules/{rule_id}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
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
    rule_id: str,
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Response[RuleRuleResponse]:
    """Edit a specific Rule

     The ability to modify the details of a specific rule based on the rule's unique reference.

    Args:
        rule_id (str):
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    kwargs = _get_kwargs(
        rule_id=rule_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rule_id: str,
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Optional[RuleRuleResponse]:
    """Edit a specific Rule

     The ability to modify the details of a specific rule based on the rule's unique reference.

    Args:
        rule_id (str):
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    return sync_detailed(
        rule_id=rule_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    rule_id: str,
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Response[RuleRuleResponse]:
    """Edit a specific Rule

     The ability to modify the details of a specific rule based on the rule's unique reference.

    Args:
        rule_id (str):
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    kwargs = _get_kwargs(
        rule_id=rule_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rule_id: str,
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Optional[RuleRuleResponse]:
    """Edit a specific Rule

     The ability to modify the details of a specific rule based on the rule's unique reference.

    Args:
        rule_id (str):
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    return (
        await asyncio_detailed(
            rule_id=rule_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
