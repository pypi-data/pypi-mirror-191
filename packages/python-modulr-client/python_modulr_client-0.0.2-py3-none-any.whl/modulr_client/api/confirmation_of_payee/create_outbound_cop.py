from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.confirmationofpayee_json_outbound_cop_error_response import (
    ConfirmationofpayeeJsonOutboundCopErrorResponse,
)
from ...models.confirmationofpayee_json_outbound_cop_request import (
    ConfirmationofpayeeJsonOutboundCopRequest,
)
from ...models.confirmationofpayee_json_outbound_cop_response import (
    ConfirmationofpayeeJsonOutboundCopResponse,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ConfirmationofpayeeJsonOutboundCopRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/account-name-check"

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
) -> Optional[
    Union[
        ConfirmationofpayeeJsonOutboundCopResponse,
        List["ConfirmationofpayeeJsonOutboundCopErrorResponse"],
    ]
]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ConfirmationofpayeeJsonOutboundCopResponse.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = []
        _response_400 = response.json()
        for response_400_item_data in _response_400:
            response_400_item = ConfirmationofpayeeJsonOutboundCopErrorResponse.from_dict(
                response_400_item_data
            )

            response_400.append(response_400_item)

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = []
        _response_404 = response.json()
        for response_404_item_data in _response_404:
            response_404_item = ConfirmationofpayeeJsonOutboundCopErrorResponse.from_dict(
                response_404_item_data
            )

            response_404.append(response_404_item)

        return response_404
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        response_429 = []
        _response_429 = response.json()
        for response_429_item_data in _response_429:
            response_429_item = ConfirmationofpayeeJsonOutboundCopErrorResponse.from_dict(
                response_429_item_data
            )

            response_429.append(response_429_item)

        return response_429
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = []
        _response_500 = response.json()
        for response_500_item_data in _response_500:
            response_500_item = ConfirmationofpayeeJsonOutboundCopErrorResponse.from_dict(
                response_500_item_data
            )

            response_500.append(response_500_item)

        return response_500
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = []
        _response_503 = response.json()
        for response_503_item_data in _response_503:
            response_503_item = ConfirmationofpayeeJsonOutboundCopErrorResponse.from_dict(
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
        ConfirmationofpayeeJsonOutboundCopResponse,
        List["ConfirmationofpayeeJsonOutboundCopErrorResponse"],
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
    json_body: ConfirmationofpayeeJsonOutboundCopRequest,
) -> Response[
    Union[
        ConfirmationofpayeeJsonOutboundCopResponse,
        List["ConfirmationofpayeeJsonOutboundCopErrorResponse"],
    ]
]:
    """Create an account name check

     This endpoint allows you to check the account details of a payee with their bank before you create a
    beneficiary or payment. If the account details are confirmed, you will have greater assurance that a
    payment you create will reach the correct bank account.
    This endpoint does not support idempotent requests. Any requests containing an x-mod-nonce header
    used by a previous request will return the response <code>403: Forbidden (\"Unique/allowed nonce
    header not found\")</code>

    Args:
        json_body (ConfirmationofpayeeJsonOutboundCopRequest): Details of Account Name Check
            Request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeJsonOutboundCopResponse, List['ConfirmationofpayeeJsonOutboundCopErrorResponse']]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: ConfirmationofpayeeJsonOutboundCopRequest,
) -> Optional[
    Union[
        ConfirmationofpayeeJsonOutboundCopResponse,
        List["ConfirmationofpayeeJsonOutboundCopErrorResponse"],
    ]
]:
    """Create an account name check

     This endpoint allows you to check the account details of a payee with their bank before you create a
    beneficiary or payment. If the account details are confirmed, you will have greater assurance that a
    payment you create will reach the correct bank account.
    This endpoint does not support idempotent requests. Any requests containing an x-mod-nonce header
    used by a previous request will return the response <code>403: Forbidden (\"Unique/allowed nonce
    header not found\")</code>

    Args:
        json_body (ConfirmationofpayeeJsonOutboundCopRequest): Details of Account Name Check
            Request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeJsonOutboundCopResponse, List['ConfirmationofpayeeJsonOutboundCopErrorResponse']]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ConfirmationofpayeeJsonOutboundCopRequest,
) -> Response[
    Union[
        ConfirmationofpayeeJsonOutboundCopResponse,
        List["ConfirmationofpayeeJsonOutboundCopErrorResponse"],
    ]
]:
    """Create an account name check

     This endpoint allows you to check the account details of a payee with their bank before you create a
    beneficiary or payment. If the account details are confirmed, you will have greater assurance that a
    payment you create will reach the correct bank account.
    This endpoint does not support idempotent requests. Any requests containing an x-mod-nonce header
    used by a previous request will return the response <code>403: Forbidden (\"Unique/allowed nonce
    header not found\")</code>

    Args:
        json_body (ConfirmationofpayeeJsonOutboundCopRequest): Details of Account Name Check
            Request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeJsonOutboundCopResponse, List['ConfirmationofpayeeJsonOutboundCopErrorResponse']]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: ConfirmationofpayeeJsonOutboundCopRequest,
) -> Optional[
    Union[
        ConfirmationofpayeeJsonOutboundCopResponse,
        List["ConfirmationofpayeeJsonOutboundCopErrorResponse"],
    ]
]:
    """Create an account name check

     This endpoint allows you to check the account details of a payee with their bank before you create a
    beneficiary or payment. If the account details are confirmed, you will have greater assurance that a
    payment you create will reach the correct bank account.
    This endpoint does not support idempotent requests. Any requests containing an x-mod-nonce header
    used by a previous request will return the response <code>403: Forbidden (\"Unique/allowed nonce
    header not found\")</code>

    Args:
        json_body (ConfirmationofpayeeJsonOutboundCopRequest): Details of Account Name Check
            Request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ConfirmationofpayeeJsonOutboundCopResponse, List['ConfirmationofpayeeJsonOutboundCopErrorResponse']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
