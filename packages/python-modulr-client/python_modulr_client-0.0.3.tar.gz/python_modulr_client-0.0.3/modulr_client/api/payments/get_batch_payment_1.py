from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.payment_batch_payment_details_response import (
    PaymentBatchPaymentDetailsResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    include_payments: Union[Unset, None, bool] = True,
) -> Dict[str, Any]:
    url = f"{client.base_url}/batchpayments/{id}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["includePayments"] = include_payments

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
) -> Optional[PaymentBatchPaymentDetailsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaymentBatchPaymentDetailsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PaymentBatchPaymentDetailsResponse]:
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
    include_payments: Union[Unset, None, bool] = True,
) -> Response[PaymentBatchPaymentDetailsResponse]:
    """Retrieve details of a batch payment

     As well as supporting individual payment requests, the Modulr payment platform can also handle
    multiple payment objects in the same request. This endpoint is to get the details of a batch payment
    that has already been created, via the unique reference that was in the response to the original
    batch payment request.

    Args:
        id (str):
        include_payments (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentDetailsResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        include_payments=include_payments,
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
    include_payments: Union[Unset, None, bool] = True,
) -> Optional[PaymentBatchPaymentDetailsResponse]:
    """Retrieve details of a batch payment

     As well as supporting individual payment requests, the Modulr payment platform can also handle
    multiple payment objects in the same request. This endpoint is to get the details of a batch payment
    that has already been created, via the unique reference that was in the response to the original
    batch payment request.

    Args:
        id (str):
        include_payments (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentDetailsResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        include_payments=include_payments,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    include_payments: Union[Unset, None, bool] = True,
) -> Response[PaymentBatchPaymentDetailsResponse]:
    """Retrieve details of a batch payment

     As well as supporting individual payment requests, the Modulr payment platform can also handle
    multiple payment objects in the same request. This endpoint is to get the details of a batch payment
    that has already been created, via the unique reference that was in the response to the original
    batch payment request.

    Args:
        id (str):
        include_payments (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentDetailsResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        include_payments=include_payments,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    include_payments: Union[Unset, None, bool] = True,
) -> Optional[PaymentBatchPaymentDetailsResponse]:
    """Retrieve details of a batch payment

     As well as supporting individual payment requests, the Modulr payment platform can also handle
    multiple payment objects in the same request. This endpoint is to get the details of a batch payment
    that has already been created, via the unique reference that was in the response to the original
    batch payment request.

    Args:
        id (str):
        include_payments (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentDetailsResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            include_payments=include_payments,
        )
    ).parsed
