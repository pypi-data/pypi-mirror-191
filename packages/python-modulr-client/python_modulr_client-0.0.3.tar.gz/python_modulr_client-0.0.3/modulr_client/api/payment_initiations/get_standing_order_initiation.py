from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.pispgateway_get_standing_order_initiation_response import (
    PispgatewayGetStandingOrderInitiationResponse,
)
from ...types import Response


def _get_kwargs(
    standing_order_initiation_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/standing-order-initiations/{standingOrderInitiationId}".format(
        client.base_url, standingOrderInitiationId=standing_order_initiation_id
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
) -> Optional[PispgatewayGetStandingOrderInitiationResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PispgatewayGetStandingOrderInitiationResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = PispgatewayGetStandingOrderInitiationResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PispgatewayGetStandingOrderInitiationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    standing_order_initiation_id: str,
    *,
    client: Client,
) -> Response[PispgatewayGetStandingOrderInitiationResponse]:
    """Get standing order initiation request details

     Retrieve the details of a specific standing order initiation request.

    Args:
        standing_order_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetStandingOrderInitiationResponse]
    """

    kwargs = _get_kwargs(
        standing_order_initiation_id=standing_order_initiation_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    standing_order_initiation_id: str,
    *,
    client: Client,
) -> Optional[PispgatewayGetStandingOrderInitiationResponse]:
    """Get standing order initiation request details

     Retrieve the details of a specific standing order initiation request.

    Args:
        standing_order_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetStandingOrderInitiationResponse]
    """

    return sync_detailed(
        standing_order_initiation_id=standing_order_initiation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    standing_order_initiation_id: str,
    *,
    client: Client,
) -> Response[PispgatewayGetStandingOrderInitiationResponse]:
    """Get standing order initiation request details

     Retrieve the details of a specific standing order initiation request.

    Args:
        standing_order_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetStandingOrderInitiationResponse]
    """

    kwargs = _get_kwargs(
        standing_order_initiation_id=standing_order_initiation_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    standing_order_initiation_id: str,
    *,
    client: Client,
) -> Optional[PispgatewayGetStandingOrderInitiationResponse]:
    """Get standing order initiation request details

     Retrieve the details of a specific standing order initiation request.

    Args:
        standing_order_initiation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PispgatewayGetStandingOrderInitiationResponse]
    """

    return (
        await asyncio_detailed(
            standing_order_initiation_id=standing_order_initiation_id,
            client=client,
        )
    ).parsed
