from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.account_account_response import AccountAccountResponse
from ...models.account_update_account_request import AccountUpdateAccountRequest
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: AccountUpdateAccountRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/accounts/{id}"

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
    json_body: AccountUpdateAccountRequest,
) -> Response[AccountAccountResponse]:
    """Edit an account

     Edit details of a particular account using its ID as a reference
    Currently editable fields:
      1. for accounts of all customer types, externalReference can be edited
      2. for accounts of PCM_INDIVIDUAL & PCM_BUSINESS customer types, name can additionally be edited

    Args:
        id (str):
        json_body (AccountUpdateAccountRequest): Details of account to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: AccountUpdateAccountRequest,
) -> Optional[AccountAccountResponse]:
    """Edit an account

     Edit details of a particular account using its ID as a reference
    Currently editable fields:
      1. for accounts of all customer types, externalReference can be edited
      2. for accounts of PCM_INDIVIDUAL & PCM_BUSINESS customer types, name can additionally be edited

    Args:
        id (str):
        json_body (AccountUpdateAccountRequest): Details of account to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: AccountUpdateAccountRequest,
) -> Response[AccountAccountResponse]:
    """Edit an account

     Edit details of a particular account using its ID as a reference
    Currently editable fields:
      1. for accounts of all customer types, externalReference can be edited
      2. for accounts of PCM_INDIVIDUAL & PCM_BUSINESS customer types, name can additionally be edited

    Args:
        id (str):
        json_body (AccountUpdateAccountRequest): Details of account to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountAccountResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: AccountUpdateAccountRequest,
) -> Optional[AccountAccountResponse]:
    """Edit an account

     Edit details of a particular account using its ID as a reference
    Currently editable fields:
      1. for accounts of all customer types, externalReference can be edited
      2. for accounts of PCM_INDIVIDUAL & PCM_BUSINESS customer types, name can additionally be edited

    Args:
        id (str):
        json_body (AccountUpdateAccountRequest): Details of account to edit

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
            json_body=json_body,
        )
    ).parsed
