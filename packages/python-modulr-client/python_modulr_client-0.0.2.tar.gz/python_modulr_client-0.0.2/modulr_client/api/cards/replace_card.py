from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.card_card_replacement_request import CardCardReplacementRequest
from ...models.card_card_replacement_response import CardCardReplacementResponse
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: CardCardReplacementRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/cards/{id}/replace"

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
) -> Optional[CardCardReplacementResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CardCardReplacementResponse.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardCardReplacementResponse]:
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
    json_body: CardCardReplacementRequest,
) -> Response[CardCardReplacementResponse]:
    """Replace a card

     Replace a card, with a reason STOLEN, DAMAGED, LOST, RENEW.

    Args:
        id (str):
        json_body (CardCardReplacementRequest): Replacement

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardReplacementResponse]
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
    json_body: CardCardReplacementRequest,
) -> Optional[CardCardReplacementResponse]:
    """Replace a card

     Replace a card, with a reason STOLEN, DAMAGED, LOST, RENEW.

    Args:
        id (str):
        json_body (CardCardReplacementRequest): Replacement

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardReplacementResponse]
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
    json_body: CardCardReplacementRequest,
) -> Response[CardCardReplacementResponse]:
    """Replace a card

     Replace a card, with a reason STOLEN, DAMAGED, LOST, RENEW.

    Args:
        id (str):
        json_body (CardCardReplacementRequest): Replacement

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardReplacementResponse]
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
    json_body: CardCardReplacementRequest,
) -> Optional[CardCardReplacementResponse]:
    """Replace a card

     Replace a card, with a reason STOLEN, DAMAGED, LOST, RENEW.

    Args:
        id (str):
        json_body (CardCardReplacementRequest): Replacement

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardReplacementResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
