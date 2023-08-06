from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.notification_notification_response import (
    NotificationNotificationResponse,
)
from ...models.notification_update_notification_request import (
    NotificationUpdateNotificationRequest,
)
from ...types import Response


def _get_kwargs(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
    json_body: NotificationUpdateNotificationRequest,
) -> Dict[str, Any]:
    url = "{}/partners/{partnerId}/notifications/{notificationId}".format(
        client.base_url, partnerId=partner_id, notificationId=notification_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
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
    json_body: NotificationUpdateNotificationRequest,
) -> Response[NotificationNotificationResponse]:
    """Update a specific notification by unique reference for a specific partner

     If you need to change anything about a particular notification, for example add an email address or
    make it inactive, then this is the endpoint to use. You need to put all of the information into this
    request for the notification even if it isn't changing, so either you will need to record this
    somewhere when you create the notification, or call the 'GET' request first.

    Args:
        partner_id (str):
        notification_id (str):
        json_body (NotificationUpdateNotificationRequest):

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
        json_body=json_body,
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
    json_body: NotificationUpdateNotificationRequest,
) -> Optional[NotificationNotificationResponse]:
    """Update a specific notification by unique reference for a specific partner

     If you need to change anything about a particular notification, for example add an email address or
    make it inactive, then this is the endpoint to use. You need to put all of the information into this
    request for the notification even if it isn't changing, so either you will need to record this
    somewhere when you create the notification, or call the 'GET' request first.

    Args:
        partner_id (str):
        notification_id (str):
        json_body (NotificationUpdateNotificationRequest):

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
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
    json_body: NotificationUpdateNotificationRequest,
) -> Response[NotificationNotificationResponse]:
    """Update a specific notification by unique reference for a specific partner

     If you need to change anything about a particular notification, for example add an email address or
    make it inactive, then this is the endpoint to use. You need to put all of the information into this
    request for the notification even if it isn't changing, so either you will need to record this
    somewhere when you create the notification, or call the 'GET' request first.

    Args:
        partner_id (str):
        notification_id (str):
        json_body (NotificationUpdateNotificationRequest):

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
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    partner_id: str,
    notification_id: str,
    *,
    client: Client,
    json_body: NotificationUpdateNotificationRequest,
) -> Optional[NotificationNotificationResponse]:
    """Update a specific notification by unique reference for a specific partner

     If you need to change anything about a particular notification, for example add an email address or
    make it inactive, then this is the endpoint to use. You need to put all of the information into this
    request for the notification even if it isn't changing, so either you will need to record this
    somewhere when you create the notification, or call the 'GET' request first.

    Args:
        partner_id (str):
        notification_id (str):
        json_body (NotificationUpdateNotificationRequest):

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
            json_body=json_body,
        )
    ).parsed
