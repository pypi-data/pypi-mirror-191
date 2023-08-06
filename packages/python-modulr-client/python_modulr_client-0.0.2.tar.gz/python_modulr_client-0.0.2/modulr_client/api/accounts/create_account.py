from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.account_account_response import AccountAccountResponse
from ...models.account_create_account_request import AccountCreateAccountRequest
from ...types import Response


def _get_kwargs(
    customer_id: str,
    *,
    client: Client,
    json_body: AccountCreateAccountRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers/{customer_id}/accounts"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[AccountAccountResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = AccountAccountResponse.from_dict(response.json())

        return response_201
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
    customer_id: str,
    *,
    client: Client,
    json_body: AccountCreateAccountRequest,
) -> Response[AccountAccountResponse]:
    """Create account by customer

     Creates an account for a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        json_body (AccountCreateAccountRequest): Details of account to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        json_body=json_body,
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
    json_body: AccountCreateAccountRequest,
) -> Optional[AccountAccountResponse]:
    """Create account by customer

     Creates an account for a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        json_body (AccountCreateAccountRequest): Details of account to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    return sync_detailed(
        customer_id=customer_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    customer_id: str,
    *,
    client: Client,
    json_body: AccountCreateAccountRequest,
) -> Response[AccountAccountResponse]:
    """Create account by customer

     Creates an account for a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        json_body (AccountCreateAccountRequest): Details of account to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    customer_id: str,
    *,
    client: Client,
    json_body: AccountCreateAccountRequest,
) -> Optional[AccountAccountResponse]:
    """Create account by customer

     Creates an account for a particular customer using the customer’s ID as a reference

    Args:
        customer_id (str):
        json_body (AccountCreateAccountRequest): Details of account to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    return (
        await asyncio_detailed(
            customer_id=customer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
