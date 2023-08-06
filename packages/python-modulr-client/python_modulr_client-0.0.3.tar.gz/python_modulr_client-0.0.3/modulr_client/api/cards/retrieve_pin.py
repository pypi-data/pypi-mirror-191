from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.card_card_pin_response import CardCardPinResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/cards/{id}/pin"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(x_mod_card_mgmt_token, Unset):
        headers["X-MOD-CARD-MGMT-TOKEN"] = x_mod_card_mgmt_token

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CardCardPinResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CardCardPinResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CardCardPinResponse.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CardCardPinResponse]:
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
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Response[CardCardPinResponse]:
    """Retrieve PIN

     Retrieves the PIN for a card, as a reminder for the cardholder

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPinResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
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
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Optional[CardCardPinResponse]:
    """Retrieve PIN

     Retrieves the PIN for a card, as a reminder for the cardholder

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPinResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Response[CardCardPinResponse]:
    """Retrieve PIN

     Retrieves the PIN for a card, as a reminder for the cardholder

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPinResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Optional[CardCardPinResponse]:
    """Retrieve PIN

     Retrieves the PIN for a card, as a reminder for the cardholder

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCardPinResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            x_mod_card_mgmt_token=x_mod_card_mgmt_token,
        )
    ).parsed
