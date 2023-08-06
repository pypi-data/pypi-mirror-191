from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.paymentfileupload_file_upload_request import (
    PaymentfileuploadFileUploadRequest,
)
from ...models.paymentfileupload_file_upload_response import (
    PaymentfileuploadFileUploadResponse,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: PaymentfileuploadFileUploadRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/payment-files"

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
) -> Optional[PaymentfileuploadFileUploadResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaymentfileuploadFileUploadResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = PaymentfileuploadFileUploadResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PaymentfileuploadFileUploadResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: PaymentfileuploadFileUploadRequest,
) -> Response[PaymentfileuploadFileUploadResponse]:
    """Upload payment file and store valid payments

     Uploads the payment file and store the valid files extracted payments for later creating payments

    Args:
        json_body (PaymentfileuploadFileUploadRequest): File upload request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileUploadResponse]
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
    json_body: PaymentfileuploadFileUploadRequest,
) -> Optional[PaymentfileuploadFileUploadResponse]:
    """Upload payment file and store valid payments

     Uploads the payment file and store the valid files extracted payments for later creating payments

    Args:
        json_body (PaymentfileuploadFileUploadRequest): File upload request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileUploadResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: PaymentfileuploadFileUploadRequest,
) -> Response[PaymentfileuploadFileUploadResponse]:
    """Upload payment file and store valid payments

     Uploads the payment file and store the valid files extracted payments for later creating payments

    Args:
        json_body (PaymentfileuploadFileUploadRequest): File upload request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileUploadResponse]
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
    json_body: PaymentfileuploadFileUploadRequest,
) -> Optional[PaymentfileuploadFileUploadResponse]:
    """Upload payment file and store valid payments

     Uploads the payment file and store the valid files extracted payments for later creating payments

    Args:
        json_body (PaymentfileuploadFileUploadRequest): File upload request body

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentfileuploadFileUploadResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
