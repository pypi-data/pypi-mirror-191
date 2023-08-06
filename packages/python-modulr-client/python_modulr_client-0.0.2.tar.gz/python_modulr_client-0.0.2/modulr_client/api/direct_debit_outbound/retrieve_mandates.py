from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.directdebitoutbound_enquiry_mandates_response import (
    DirectdebitoutboundEnquiryMandatesResponse,
)
from ...types import Response


def _get_kwargs(
    account_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = f"{client.base_url}/directdebits/enquire/{account_id}"

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[DirectdebitoutboundEnquiryMandatesResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DirectdebitoutboundEnquiryMandatesResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[DirectdebitoutboundEnquiryMandatesResponse]:
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
) -> Response[DirectdebitoutboundEnquiryMandatesResponse]:
    """Retrieve all Mandates for an account

     Used to get all the Mandates for a specific account.

    Args:
        account_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitoutboundEnquiryMandatesResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        client=client,
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
) -> Optional[DirectdebitoutboundEnquiryMandatesResponse]:
    """Retrieve all Mandates for an account

     Used to get all the Mandates for a specific account.

    Args:
        account_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitoutboundEnquiryMandatesResponse]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Client,
) -> Response[DirectdebitoutboundEnquiryMandatesResponse]:
    """Retrieve all Mandates for an account

     Used to get all the Mandates for a specific account.

    Args:
        account_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitoutboundEnquiryMandatesResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Client,
) -> Optional[DirectdebitoutboundEnquiryMandatesResponse]:
    """Retrieve all Mandates for an account

     Used to get all the Mandates for a specific account.

    Args:
        account_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitoutboundEnquiryMandatesResponse]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
        )
    ).parsed
