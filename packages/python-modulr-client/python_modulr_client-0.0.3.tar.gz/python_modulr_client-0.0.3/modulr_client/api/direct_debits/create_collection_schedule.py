from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.directdebit_collection_schedule_response import (
    DirectdebitCollectionScheduleResponse,
)
from ...models.directdebit_create_collection_schedule_request import (
    DirectdebitCreateCollectionScheduleRequest,
)
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: DirectdebitCreateCollectionScheduleRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/mandates/{id}/collectionschedules"

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
) -> Optional[DirectdebitCollectionScheduleResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DirectdebitCollectionScheduleResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[DirectdebitCollectionScheduleResponse]:
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
    json_body: DirectdebitCreateCollectionScheduleRequest,
) -> Response[DirectdebitCollectionScheduleResponse]:
    """Create the collection schedule for the given mandate-id.

     Creates a Direct Debit collection schedule; the agreed to framework for the collections for the
    given mandate-id. This could be a single collection or multiple and includes the frequency and
    amounts of the planned payments.

    Args:
        id (str):
        json_body (DirectdebitCreateCollectionScheduleRequest): Details of collection to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitCollectionScheduleResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: DirectdebitCreateCollectionScheduleRequest,
) -> Optional[DirectdebitCollectionScheduleResponse]:
    """Create the collection schedule for the given mandate-id.

     Creates a Direct Debit collection schedule; the agreed to framework for the collections for the
    given mandate-id. This could be a single collection or multiple and includes the frequency and
    amounts of the planned payments.

    Args:
        id (str):
        json_body (DirectdebitCreateCollectionScheduleRequest): Details of collection to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitCollectionScheduleResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: DirectdebitCreateCollectionScheduleRequest,
) -> Response[DirectdebitCollectionScheduleResponse]:
    """Create the collection schedule for the given mandate-id.

     Creates a Direct Debit collection schedule; the agreed to framework for the collections for the
    given mandate-id. This could be a single collection or multiple and includes the frequency and
    amounts of the planned payments.

    Args:
        id (str):
        json_body (DirectdebitCreateCollectionScheduleRequest): Details of collection to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitCollectionScheduleResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: DirectdebitCreateCollectionScheduleRequest,
) -> Optional[DirectdebitCollectionScheduleResponse]:
    """Create the collection schedule for the given mandate-id.

     Creates a Direct Debit collection schedule; the agreed to framework for the collections for the
    given mandate-id. This could be a single collection or multiple and includes the frequency and
    amounts of the planned payments.

    Args:
        id (str):
        json_body (DirectdebitCreateCollectionScheduleRequest): Details of collection to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectdebitCollectionScheduleResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
