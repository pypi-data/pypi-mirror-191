from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.notification_notification_request import NotificationNotificationRequest
from ...models.notification_notification_response import (
    NotificationNotificationResponse,
)
from ...types import Response


def _get_kwargs(
    customer_id: str,
    *,
    client: Client,
    json_body: NotificationNotificationRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers/{customer_id}/notifications"

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
) -> Optional[NotificationNotificationResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = NotificationNotificationResponse.from_dict(response.json())

        return response_201
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
    customer_id: str,
    *,
    client: Client,
    json_body: NotificationNotificationRequest,
) -> Response[NotificationNotificationResponse]:
    """Set up a Notification for a Customer

     Sets up a new notification for a customer using the customer's ID as a reference. Returns a
    notification ID that should be saved if the notification needs to be amended in the future

    Args:
        customer_id (str):
        json_body (NotificationNotificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    customer_id: str,
    *,
    client: Client,
    json_body: NotificationNotificationRequest,
) -> Optional[NotificationNotificationResponse]:
    """Set up a Notification for a Customer

     Sets up a new notification for a customer using the customer's ID as a reference. Returns a
    notification ID that should be saved if the notification needs to be amended in the future

    Args:
        customer_id (str):
        json_body (NotificationNotificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    return sync_detailed(
        customer_id=customer_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    customer_id: str,
    *,
    client: Client,
    json_body: NotificationNotificationRequest,
) -> Response[NotificationNotificationResponse]:
    """Set up a Notification for a Customer

     Sets up a new notification for a customer using the customer's ID as a reference. Returns a
    notification ID that should be saved if the notification needs to be amended in the future

    Args:
        customer_id (str):
        json_body (NotificationNotificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    customer_id: str,
    *,
    client: Client,
    json_body: NotificationNotificationRequest,
) -> Optional[NotificationNotificationResponse]:
    """Set up a Notification for a Customer

     Sets up a new notification for a customer using the customer's ID as a reference. Returns a
    notification ID that should be saved if the notification needs to be amended in the future

    Args:
        customer_id (str):
        json_body (NotificationNotificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NotificationNotificationResponse]
    """

    return (
        await asyncio_detailed(
            customer_id=customer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
