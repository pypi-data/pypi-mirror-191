from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.confirmationofpayee_cop_page_response_json_srd_account import (
    ConfirmationofpayeeCopPageResponseJsonSrdAccount,
)
from ...models.confirmationofpayee_message_response import (
    ConfirmationofpayeeMessageResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 500,
) -> Dict[str, Any]:
    url = f"{client.base_url}/account-name-check/srd-accounts"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["size"] = size

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        ConfirmationofpayeeCopPageResponseJsonSrdAccount,
        List["ConfirmationofpayeeMessageResponse"],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConfirmationofpayeeCopPageResponseJsonSrdAccount.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = []
        _response_400 = response.json()
        for response_400_item_data in _response_400:
            response_400_item = ConfirmationofpayeeMessageResponse.from_dict(
                response_400_item_data
            )

            response_400.append(response_400_item)

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = []
        _response_401 = response.json()
        for response_401_item_data in _response_401:
            response_401_item = ConfirmationofpayeeMessageResponse.from_dict(
                response_401_item_data
            )

            response_401.append(response_401_item)

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = []
        _response_403 = response.json()
        for response_403_item_data in _response_403:
            response_403_item = ConfirmationofpayeeMessageResponse.from_dict(
                response_403_item_data
            )

            response_403.append(response_403_item)

        return response_403
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = []
        _response_500 = response.json()
        for response_500_item_data in _response_500:
            response_500_item = ConfirmationofpayeeMessageResponse.from_dict(
                response_500_item_data
            )

            response_500.append(response_500_item)

        return response_500
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = []
        _response_503 = response.json()
        for response_503_item_data in _response_503:
            response_503_item = ConfirmationofpayeeMessageResponse.from_dict(
                response_503_item_data
            )

            response_503.append(response_503_item)

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ConfirmationofpayeeCopPageResponseJsonSrdAccount,
        List["ConfirmationofpayeeMessageResponse"],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 500,
) -> Response[
    Union[
        ConfirmationofpayeeCopPageResponseJsonSrdAccount,
        List["ConfirmationofpayeeMessageResponse"],
    ]
]:
    """Get SRD Accounts

     Returns a list of all sort codes and account numbers for which Secondary Reference Data must be
    provided with all account name check requests.

    Args:
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 500.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeCopPageResponseJsonSrdAccount, List['ConfirmationofpayeeMessageResponse']]]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        size=size,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 500,
) -> Optional[
    Union[
        ConfirmationofpayeeCopPageResponseJsonSrdAccount,
        List["ConfirmationofpayeeMessageResponse"],
    ]
]:
    """Get SRD Accounts

     Returns a list of all sort codes and account numbers for which Secondary Reference Data must be
    provided with all account name check requests.

    Args:
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 500.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeCopPageResponseJsonSrdAccount, List['ConfirmationofpayeeMessageResponse']]]
    """

    return sync_detailed(
        client=client,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 500,
) -> Response[
    Union[
        ConfirmationofpayeeCopPageResponseJsonSrdAccount,
        List["ConfirmationofpayeeMessageResponse"],
    ]
]:
    """Get SRD Accounts

     Returns a list of all sort codes and account numbers for which Secondary Reference Data must be
    provided with all account name check requests.

    Args:
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 500.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeCopPageResponseJsonSrdAccount, List['ConfirmationofpayeeMessageResponse']]]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 500,
) -> Optional[
    Union[
        ConfirmationofpayeeCopPageResponseJsonSrdAccount,
        List["ConfirmationofpayeeMessageResponse"],
    ]
]:
    """Get SRD Accounts

     Returns a list of all sort codes and account numbers for which Secondary Reference Data must be
    provided with all account name check requests.

    Args:
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 500.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeCopPageResponseJsonSrdAccount, List['ConfirmationofpayeeMessageResponse']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            size=size,
        )
    ).parsed
