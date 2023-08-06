from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.payment_payment_page_response import PaymentPaymentPageResponse
from ...models.payment_status_item import PaymentStatusItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    source_account_id: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[PaymentStatusItem]] = UNSET,
    type: Union[Unset, None, str] = "PAYOUT",
    exclude_batch_payments: Union[Unset, None, bool] = False,
    batch_payment_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/payments"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["id"] = id

    params["fromCreatedDate"] = from_created_date

    params["toCreatedDate"] = to_created_date

    params["modifiedSince"] = modified_since

    params["sourceAccountId"] = source_account_id

    params["hasExternalReference"] = has_external_reference

    params["externalReference"] = external_reference

    json_status: Union[Unset, None, List[str]] = UNSET
    if not isinstance(status, Unset):
        if status is None:
            json_status = None
        else:
            json_status = []
            for componentsschemaspayment_status_item_data in status:
                componentsschemaspayment_status_item = (
                    componentsschemaspayment_status_item_data.value
                )

                json_status.append(componentsschemaspayment_status_item)

    params["status"] = json_status

    params["type"] = type

    params["excludeBatchPayments"] = exclude_batch_payments

    params["batchPaymentId"] = batch_payment_id

    params["page"] = page

    params["size"] = size

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
) -> Optional[PaymentPaymentPageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaymentPaymentPageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PaymentPaymentPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    source_account_id: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[PaymentStatusItem]] = UNSET,
    type: Union[Unset, None, str] = "PAYOUT",
    exclude_batch_payments: Union[Unset, None, bool] = False,
    batch_payment_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = UNSET,
) -> Response[PaymentPaymentPageResponse]:
    """Retrieve payments

     The ability to get the details of payments using various pieces of information, e.g. using Account
    ID, retrieve all payments in that account. Can get details of one particular payment based on the
    unique payment reference number.

    Args:
        id (Union[Unset, None, str]): Payment ID. If specified then all other parameters are
            ignored
        from_created_date (Union[Unset, None, str]): Payments created date equal or after to this
            date. Mandatory Parameter(except when 'id' or 'modifiedSince' parameter is used) Example:
            2016-01-01T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Payments created date equal or before to this
            date
        modified_since (Union[Unset, None, str]): Payments modified date equal or before to this
            date
        source_account_id (Union[Unset, None, str]): The source account ID
        has_external_reference (Union[Unset, None, bool]): True if the API should return all items
            that have externalReference. False the API should return all items that don't have
            externalReference
        external_reference (Union[Unset, None, str]): External reference can only have
            alphanumeric characters plus underscore, hyphen and space
        status (Union[Unset, None, List[PaymentStatusItem]]):
        type (Union[Unset, None, str]): The payment type to search for. Default: 'PAYOUT'.
        exclude_batch_payments (Union[Unset, None, bool]): Exclude batch payments
        batch_payment_id (Union[Unset, None, str]): Filter on batch
        page (Union[Unset, None, str]): The page to fetch. 0 indexed Default: '0'.
        size (Union[Unset, None, str]): The size of the page(s)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentPaymentPageResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        modified_since=modified_since,
        source_account_id=source_account_id,
        has_external_reference=has_external_reference,
        external_reference=external_reference,
        status=status,
        type=type,
        exclude_batch_payments=exclude_batch_payments,
        batch_payment_id=batch_payment_id,
        page=page,
        size=size,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    source_account_id: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[PaymentStatusItem]] = UNSET,
    type: Union[Unset, None, str] = "PAYOUT",
    exclude_batch_payments: Union[Unset, None, bool] = False,
    batch_payment_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = UNSET,
) -> Optional[PaymentPaymentPageResponse]:
    """Retrieve payments

     The ability to get the details of payments using various pieces of information, e.g. using Account
    ID, retrieve all payments in that account. Can get details of one particular payment based on the
    unique payment reference number.

    Args:
        id (Union[Unset, None, str]): Payment ID. If specified then all other parameters are
            ignored
        from_created_date (Union[Unset, None, str]): Payments created date equal or after to this
            date. Mandatory Parameter(except when 'id' or 'modifiedSince' parameter is used) Example:
            2016-01-01T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Payments created date equal or before to this
            date
        modified_since (Union[Unset, None, str]): Payments modified date equal or before to this
            date
        source_account_id (Union[Unset, None, str]): The source account ID
        has_external_reference (Union[Unset, None, bool]): True if the API should return all items
            that have externalReference. False the API should return all items that don't have
            externalReference
        external_reference (Union[Unset, None, str]): External reference can only have
            alphanumeric characters plus underscore, hyphen and space
        status (Union[Unset, None, List[PaymentStatusItem]]):
        type (Union[Unset, None, str]): The payment type to search for. Default: 'PAYOUT'.
        exclude_batch_payments (Union[Unset, None, bool]): Exclude batch payments
        batch_payment_id (Union[Unset, None, str]): Filter on batch
        page (Union[Unset, None, str]): The page to fetch. 0 indexed Default: '0'.
        size (Union[Unset, None, str]): The size of the page(s)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentPaymentPageResponse]
    """

    return sync_detailed(
        client=client,
        id=id,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        modified_since=modified_since,
        source_account_id=source_account_id,
        has_external_reference=has_external_reference,
        external_reference=external_reference,
        status=status,
        type=type,
        exclude_batch_payments=exclude_batch_payments,
        batch_payment_id=batch_payment_id,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    source_account_id: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[PaymentStatusItem]] = UNSET,
    type: Union[Unset, None, str] = "PAYOUT",
    exclude_batch_payments: Union[Unset, None, bool] = False,
    batch_payment_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = UNSET,
) -> Response[PaymentPaymentPageResponse]:
    """Retrieve payments

     The ability to get the details of payments using various pieces of information, e.g. using Account
    ID, retrieve all payments in that account. Can get details of one particular payment based on the
    unique payment reference number.

    Args:
        id (Union[Unset, None, str]): Payment ID. If specified then all other parameters are
            ignored
        from_created_date (Union[Unset, None, str]): Payments created date equal or after to this
            date. Mandatory Parameter(except when 'id' or 'modifiedSince' parameter is used) Example:
            2016-01-01T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Payments created date equal or before to this
            date
        modified_since (Union[Unset, None, str]): Payments modified date equal or before to this
            date
        source_account_id (Union[Unset, None, str]): The source account ID
        has_external_reference (Union[Unset, None, bool]): True if the API should return all items
            that have externalReference. False the API should return all items that don't have
            externalReference
        external_reference (Union[Unset, None, str]): External reference can only have
            alphanumeric characters plus underscore, hyphen and space
        status (Union[Unset, None, List[PaymentStatusItem]]):
        type (Union[Unset, None, str]): The payment type to search for. Default: 'PAYOUT'.
        exclude_batch_payments (Union[Unset, None, bool]): Exclude batch payments
        batch_payment_id (Union[Unset, None, str]): Filter on batch
        page (Union[Unset, None, str]): The page to fetch. 0 indexed Default: '0'.
        size (Union[Unset, None, str]): The size of the page(s)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentPaymentPageResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        modified_since=modified_since,
        source_account_id=source_account_id,
        has_external_reference=has_external_reference,
        external_reference=external_reference,
        status=status,
        type=type,
        exclude_batch_payments=exclude_batch_payments,
        batch_payment_id=batch_payment_id,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    modified_since: Union[Unset, None, str] = UNSET,
    source_account_id: Union[Unset, None, str] = UNSET,
    has_external_reference: Union[Unset, None, bool] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[PaymentStatusItem]] = UNSET,
    type: Union[Unset, None, str] = "PAYOUT",
    exclude_batch_payments: Union[Unset, None, bool] = False,
    batch_payment_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = UNSET,
) -> Optional[PaymentPaymentPageResponse]:
    """Retrieve payments

     The ability to get the details of payments using various pieces of information, e.g. using Account
    ID, retrieve all payments in that account. Can get details of one particular payment based on the
    unique payment reference number.

    Args:
        id (Union[Unset, None, str]): Payment ID. If specified then all other parameters are
            ignored
        from_created_date (Union[Unset, None, str]): Payments created date equal or after to this
            date. Mandatory Parameter(except when 'id' or 'modifiedSince' parameter is used) Example:
            2016-01-01T01:01:01+0000.
        to_created_date (Union[Unset, None, str]): Payments created date equal or before to this
            date
        modified_since (Union[Unset, None, str]): Payments modified date equal or before to this
            date
        source_account_id (Union[Unset, None, str]): The source account ID
        has_external_reference (Union[Unset, None, bool]): True if the API should return all items
            that have externalReference. False the API should return all items that don't have
            externalReference
        external_reference (Union[Unset, None, str]): External reference can only have
            alphanumeric characters plus underscore, hyphen and space
        status (Union[Unset, None, List[PaymentStatusItem]]):
        type (Union[Unset, None, str]): The payment type to search for. Default: 'PAYOUT'.
        exclude_batch_payments (Union[Unset, None, bool]): Exclude batch payments
        batch_payment_id (Union[Unset, None, str]): Filter on batch
        page (Union[Unset, None, str]): The page to fetch. 0 indexed Default: '0'.
        size (Union[Unset, None, str]): The size of the page(s)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentPaymentPageResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            from_created_date=from_created_date,
            to_created_date=to_created_date,
            modified_since=modified_since,
            source_account_id=source_account_id,
            has_external_reference=has_external_reference,
            external_reference=external_reference,
            status=status,
            type=type,
            exclude_batch_payments=exclude_batch_payments,
            batch_payment_id=batch_payment_id,
            page=page,
            size=size,
        )
    ).parsed
