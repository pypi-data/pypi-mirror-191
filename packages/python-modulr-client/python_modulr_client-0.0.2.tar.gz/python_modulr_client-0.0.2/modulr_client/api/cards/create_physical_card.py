from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.card_async_task_created_response import CardAsyncTaskCreatedResponse
from ...models.card_create_physical_card_request import CardCreatePhysicalCardRequest
from ...types import Response


def _get_kwargs(
    aid: str,
    *,
    client: Client,
    json_body: CardCreatePhysicalCardRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/accounts/{aid}/physical-cards"

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
) -> Optional[CardAsyncTaskCreatedResponse]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = CardAsyncTaskCreatedResponse.from_dict(response.json())

        return response_202
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardAsyncTaskCreatedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aid: str,
    *,
    client: Client,
    json_body: CardCreatePhysicalCardRequest,
) -> Response[CardAsyncTaskCreatedResponse]:
    """Create a new physical card

     Asynchronously create a physical card. The response will include a resource to allow the client to
    check the status of the request.

    Args:
        aid (str):
        json_body (CardCreatePhysicalCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardAsyncTaskCreatedResponse]
    """

    kwargs = _get_kwargs(
        aid=aid,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aid: str,
    *,
    client: Client,
    json_body: CardCreatePhysicalCardRequest,
) -> Optional[CardAsyncTaskCreatedResponse]:
    """Create a new physical card

     Asynchronously create a physical card. The response will include a resource to allow the client to
    check the status of the request.

    Args:
        aid (str):
        json_body (CardCreatePhysicalCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardAsyncTaskCreatedResponse]
    """

    return sync_detailed(
        aid=aid,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    aid: str,
    *,
    client: Client,
    json_body: CardCreatePhysicalCardRequest,
) -> Response[CardAsyncTaskCreatedResponse]:
    """Create a new physical card

     Asynchronously create a physical card. The response will include a resource to allow the client to
    check the status of the request.

    Args:
        aid (str):
        json_body (CardCreatePhysicalCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardAsyncTaskCreatedResponse]
    """

    kwargs = _get_kwargs(
        aid=aid,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aid: str,
    *,
    client: Client,
    json_body: CardCreatePhysicalCardRequest,
) -> Optional[CardAsyncTaskCreatedResponse]:
    """Create a new physical card

     Asynchronously create a physical card. The response will include a resource to allow the client to
    check the status of the request.

    Args:
        aid (str):
        json_body (CardCreatePhysicalCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardAsyncTaskCreatedResponse]
    """

    return (
        await asyncio_detailed(
            aid=aid,
            client=client,
            json_body=json_body,
        )
    ).parsed
