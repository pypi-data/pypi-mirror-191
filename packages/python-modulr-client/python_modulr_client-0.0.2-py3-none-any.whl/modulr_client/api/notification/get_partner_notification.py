from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.notification_notification_response import (
    NotificationNotificationResponse,
)
from ...types import Response


def _get_kwargs(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/partners/{partnerId}/notifications/{notificationId}".format(
        client.base_url, partnerId=partner_id, notificationId=notification_id
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
) -> Optional[NotificationNotificationResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = NotificationNotificationResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = NotificationNotificationResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[NotificationNotificationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
) -> Response[NotificationNotificationResponse]:
    """Retrieve a specific notification by unique reference for a specific partner

     This allows you to see the settings for a particular notification that has been set up, for example
    if you want to check if it is active or the emails the notification is being sent to. It would be
    best practice to call this before updating a notification.

    Args:
        partner_id (str):
        notification_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    kwargs = _get_kwargs(
        partner_id=partner_id,
        notification_id=notification_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
) -> Optional[NotificationNotificationResponse]:
    """Retrieve a specific notification by unique reference for a specific partner

     This allows you to see the settings for a particular notification that has been set up, for example
    if you want to check if it is active or the emails the notification is being sent to. It would be
    best practice to call this before updating a notification.

    Args:
        partner_id (str):
        notification_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    return sync_detailed(
        partner_id=partner_id,
        notification_id=notification_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
) -> Response[NotificationNotificationResponse]:
    """Retrieve a specific notification by unique reference for a specific partner

     This allows you to see the settings for a particular notification that has been set up, for example
    if you want to check if it is active or the emails the notification is being sent to. It would be
    best practice to call this before updating a notification.

    Args:
        partner_id (str):
        notification_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    kwargs = _get_kwargs(
        partner_id=partner_id,
        notification_id=notification_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
) -> Optional[NotificationNotificationResponse]:
    """Retrieve a specific notification by unique reference for a specific partner

     This allows you to see the settings for a particular notification that has been set up, for example
    if you want to check if it is active or the emails the notification is being sent to. It would be
    best practice to call this before updating a notification.

    Args:
        partner_id (str):
        notification_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    return (
        await asyncio_detailed(
            partner_id=partner_id,
            notification_id=notification_id,
            client=client,
        )
    ).parsed
