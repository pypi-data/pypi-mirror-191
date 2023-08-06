from http import HTTPStatus
from typing import Any, Dict, List, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.notification_web_hook_failure_response import (
    NotificationWebHookFailureResponse,
)
from ...types import UNSET, Response


def _get_kwargs(
    webhook_id: str,
    *,
    client: Client,
    from_: str,
) -> Dict[str, Any]:
    url = f"{client.base_url}/webhooks/{webhook_id}/failures"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["from"] = from_

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
) -> Optional[List["NotificationWebHookFailureResponse"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = NotificationWebHookFailureResponse.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[List["NotificationWebHookFailureResponse"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: str,
    *,
    client: Client,
    from_: str,
) -> Response[List["NotificationWebHookFailureResponse"]]:
    """Check if a particular webhook has failed

     Only supports webhook notifications and as such uses the webhook endpoint. Request a specific
    notification ID and specify you want to see failures. (Max 50)

    Args:
        webhook_id (str):
        from_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationWebHookFailureResponse']]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        client=client,
        from_=from_,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    *,
    client: Client,
    from_: str,
) -> Optional[List["NotificationWebHookFailureResponse"]]:
    """Check if a particular webhook has failed

     Only supports webhook notifications and as such uses the webhook endpoint. Request a specific
    notification ID and specify you want to see failures. (Max 50)

    Args:
        webhook_id (str):
        from_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationWebHookFailureResponse']]
    """

    return sync_detailed(
        webhook_id=webhook_id,
        client=client,
        from_=from_,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    *,
    client: Client,
    from_: str,
) -> Response[List["NotificationWebHookFailureResponse"]]:
    """Check if a particular webhook has failed

     Only supports webhook notifications and as such uses the webhook endpoint. Request a specific
    notification ID and specify you want to see failures. (Max 50)

    Args:
        webhook_id (str):
        from_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationWebHookFailureResponse']]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        client=client,
        from_=from_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    *,
    client: Client,
    from_: str,
) -> Optional[List["NotificationWebHookFailureResponse"]]:
    """Check if a particular webhook has failed

     Only supports webhook notifications and as such uses the webhook endpoint. Request a specific
    notification ID and specify you want to see failures. (Max 50)

    Args:
        webhook_id (str):
        from_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['NotificationWebHookFailureResponse']]
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            client=client,
            from_=from_,
        )
    ).parsed
