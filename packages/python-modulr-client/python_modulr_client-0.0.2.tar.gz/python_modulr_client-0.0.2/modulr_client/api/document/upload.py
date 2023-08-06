from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.document_document_response import DocumentDocumentResponse
from ...models.document_document_upload_request import DocumentDocumentUploadRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: DocumentDocumentUploadRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/documents"

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
) -> Optional[DocumentDocumentResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = DocumentDocumentResponse.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[DocumentDocumentResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: DocumentDocumentUploadRequest,
) -> Response[DocumentDocumentResponse]:
    """Uploads and stores document

     Uploads and stores document in a repository. Gives back Url encoded document path in the repository

    Args:
        json_body (DocumentDocumentUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentDocumentResponse]
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
    json_body: DocumentDocumentUploadRequest,
) -> Optional[DocumentDocumentResponse]:
    """Uploads and stores document

     Uploads and stores document in a repository. Gives back Url encoded document path in the repository

    Args:
        json_body (DocumentDocumentUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentDocumentResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: DocumentDocumentUploadRequest,
) -> Response[DocumentDocumentResponse]:
    """Uploads and stores document

     Uploads and stores document in a repository. Gives back Url encoded document path in the repository

    Args:
        json_body (DocumentDocumentUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentDocumentResponse]
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
    json_body: DocumentDocumentUploadRequest,
) -> Optional[DocumentDocumentResponse]:
    """Uploads and stores document

     Uploads and stores document in a repository. Gives back Url encoded document path in the repository

    Args:
        json_body (DocumentDocumentUploadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentDocumentResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
