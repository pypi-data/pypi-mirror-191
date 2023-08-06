from http import HTTPStatus
from typing import Any, Dict, List, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.notification_notification_response import (
    NotificationNotificationResponse,
)
from ...types import Response


def _get_kwargs(
    partner_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = f"{client.base_url}/partners/{partner_id}/notifications"

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
) -> Optional[List["NotificationNotificationResponse"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = NotificationNotificationResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = []
        _response_404 = response.json()
        for response_404_item_data in _response_404:
            response_404_item = NotificationNotificationResponse.from_dict(response_404_item_data)

            response_404.append(response_404_item)

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[List["NotificationNotificationResponse"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    partner_id: str,
    *,
    client: Client,
) -> Response[List["NotificationNotificationResponse"]]:
    """Get all Notifications linked directly to a Partner

     Retrieve details of all notifications set up for a partner using the partner's ID as a reference

    Args:
        partner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationNotificationResponse']]
    """

    kwargs = _get_kwargs(
        partner_id=partner_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    partner_id: str,
    *,
    client: Client,
) -> Optional[List["NotificationNotificationResponse"]]:
    """Get all Notifications linked directly to a Partner

     Retrieve details of all notifications set up for a partner using the partner's ID as a reference

    Args:
        partner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationNotificationResponse']]
    """

    return sync_detailed(
        partner_id=partner_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    partner_id: str,
    *,
    client: Client,
) -> Response[List["NotificationNotificationResponse"]]:
    """Get all Notifications linked directly to a Partner

     Retrieve details of all notifications set up for a partner using the partner's ID as a reference

    Args:
        partner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationNotificationResponse']]
    """

    kwargs = _get_kwargs(
        partner_id=partner_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    partner_id: str,
    *,
    client: Client,
) -> Optional[List["NotificationNotificationResponse"]]:
    """Get all Notifications linked directly to a Partner

     Retrieve details of all notifications set up for a partner using the partner's ID as a reference

    Args:
        partner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationNotificationResponse']]
    """

    return (
        await asyncio_detailed(
            partner_id=partner_id,
            client=client,
        )
    ).parsed
