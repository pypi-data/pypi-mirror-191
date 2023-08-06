from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.card_one_time_token_request import CardOneTimeTokenRequest
from ...models.card_one_time_token_response import CardOneTimeTokenResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: CardOneTimeTokenRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/cards/{id}/secure-details-token"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(x_mod_card_mgmt_token, Unset):
        headers["X-MOD-CARD-MGMT-TOKEN"] = x_mod_card_mgmt_token

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
) -> Optional[CardOneTimeTokenResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CardOneTimeTokenResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardOneTimeTokenResponse]:
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
    json_body: CardOneTimeTokenRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Response[CardOneTimeTokenResponse]:
    """Create secure card details token

     Create a token that is used as a parameter to retrieve secure card details (PAN, CVV, and PIN) or to
    perform PIN alterations. This token is to be retrieved by the partner and pushed to the cardholder
    device where the call is made. The token will be valid for 60 seconds.

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):
        json_body (CardOneTimeTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardOneTimeTokenResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: CardOneTimeTokenRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Optional[CardOneTimeTokenResponse]:
    """Create secure card details token

     Create a token that is used as a parameter to retrieve secure card details (PAN, CVV, and PIN) or to
    perform PIN alterations. This token is to be retrieved by the partner and pushed to the cardholder
    device where the call is made. The token will be valid for 60 seconds.

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):
        json_body (CardOneTimeTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardOneTimeTokenResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: CardOneTimeTokenRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Response[CardOneTimeTokenResponse]:
    """Create secure card details token

     Create a token that is used as a parameter to retrieve secure card details (PAN, CVV, and PIN) or to
    perform PIN alterations. This token is to be retrieved by the partner and pushed to the cardholder
    device where the call is made. The token will be valid for 60 seconds.

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):
        json_body (CardOneTimeTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardOneTimeTokenResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: CardOneTimeTokenRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Optional[CardOneTimeTokenResponse]:
    """Create secure card details token

     Create a token that is used as a parameter to retrieve secure card details (PAN, CVV, and PIN) or to
    perform PIN alterations. This token is to be retrieved by the partner and pushed to the cardholder
    device where the call is made. The token will be valid for 60 seconds.

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):
        json_body (CardOneTimeTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardOneTimeTokenResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
            x_mod_card_mgmt_token=x_mod_card_mgmt_token,
        )
    ).parsed
