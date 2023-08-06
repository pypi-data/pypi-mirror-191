from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.pispgateway_get_payment_initiation_response import (
    PispgatewayGetPaymentInitiationResponse,
)
from ...types import Response


def _get_kwargs(
    payment_initiation_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/payment-initiations/{paymentInitiationId}".format(
        client.base_url, paymentInitiationId=payment_initiation_id
    )

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
) -> Optional[PispgatewayGetPaymentInitiationResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PispgatewayGetPaymentInitiationResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = PispgatewayGetPaymentInitiationResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PispgatewayGetPaymentInitiationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    payment_initiation_id: str,
    *,
    client: Client,
) -> Response[PispgatewayGetPaymentInitiationResponse]:
    """Get payment initiation request details

     Retrieve the details of a specific payment initiation request.

    Args:
        payment_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetPaymentInitiationResponse]
    """

    kwargs = _get_kwargs(
        payment_initiation_id=payment_initiation_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    payment_initiation_id: str,
    *,
    client: Client,
) -> Optional[PispgatewayGetPaymentInitiationResponse]:
    """Get payment initiation request details

     Retrieve the details of a specific payment initiation request.

    Args:
        payment_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetPaymentInitiationResponse]
    """

    return sync_detailed(
        payment_initiation_id=payment_initiation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    payment_initiation_id: str,
    *,
    client: Client,
) -> Response[PispgatewayGetPaymentInitiationResponse]:
    """Get payment initiation request details

     Retrieve the details of a specific payment initiation request.

    Args:
        payment_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetPaymentInitiationResponse]
    """

    kwargs = _get_kwargs(
        payment_initiation_id=payment_initiation_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    payment_initiation_id: str,
    *,
    client: Client,
) -> Optional[PispgatewayGetPaymentInitiationResponse]:
    """Get payment initiation request details

     Retrieve the details of a specific payment initiation request.

    Args:
        payment_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetPaymentInitiationResponse]
    """

    return (
        await asyncio_detailed(
            payment_initiation_id=payment_initiation_id,
            client=client,
        )
    ).parsed
