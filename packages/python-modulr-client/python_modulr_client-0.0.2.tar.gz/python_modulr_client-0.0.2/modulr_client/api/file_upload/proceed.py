from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.paymentfileupload_file_create_payments_response import (
    PaymentfileuploadFileCreatePaymentsResponse,
)
from ...models.paymentfileupload_file_create_request import (
    PaymentfileuploadFileCreateRequest,
)
from ...types import Response


def _get_kwargs(
    file_id: str,
    *,
    client: Client,
    json_body: PaymentfileuploadFileCreateRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/payment-files/{file_id}/proceed"

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
) -> Optional[PaymentfileuploadFileCreatePaymentsResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = PaymentfileuploadFileCreatePaymentsResponse.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PaymentfileuploadFileCreatePaymentsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_id: str,
    *,
    client: Client,
    json_body: PaymentfileuploadFileCreateRequest,
) -> Response[PaymentfileuploadFileCreatePaymentsResponse]:
    """Create payments from an uploaded file

     Create a batch payment request from a valid upload file and send for processing to the payment
    service

    Args:
        file_id (str):
        json_body (PaymentfileuploadFileCreateRequest): File create payments request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileCreatePaymentsResponse]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_id: str,
    *,
    client: Client,
    json_body: PaymentfileuploadFileCreateRequest,
) -> Optional[PaymentfileuploadFileCreatePaymentsResponse]:
    """Create payments from an uploaded file

     Create a batch payment request from a valid upload file and send for processing to the payment
    service

    Args:
        file_id (str):
        json_body (PaymentfileuploadFileCreateRequest): File create payments request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileCreatePaymentsResponse]
    """

    return sync_detailed(
        file_id=file_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    file_id: str,
    *,
    client: Client,
    json_body: PaymentfileuploadFileCreateRequest,
) -> Response[PaymentfileuploadFileCreatePaymentsResponse]:
    """Create payments from an uploaded file

     Create a batch payment request from a valid upload file and send for processing to the payment
    service

    Args:
        file_id (str):
        json_body (PaymentfileuploadFileCreateRequest): File create payments request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileCreatePaymentsResponse]
    """

    kwargs = _get_kwargs(
        file_id=file_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_id: str,
    *,
    client: Client,
    json_body: PaymentfileuploadFileCreateRequest,
) -> Optional[PaymentfileuploadFileCreatePaymentsResponse]:
    """Create payments from an uploaded file

     Create a batch payment request from a valid upload file and send for processing to the payment
    service

    Args:
        file_id (str):
        json_body (PaymentfileuploadFileCreateRequest): File create payments request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileCreatePaymentsResponse]
    """

    return (
        await asyncio_detailed(
            file_id=file_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
