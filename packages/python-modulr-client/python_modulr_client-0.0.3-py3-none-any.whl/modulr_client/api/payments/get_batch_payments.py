from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.payment_approval_status_item import PaymentApprovalStatusItem
from ...models.payment_batch_payment_statuses_item import (
    PaymentBatchPaymentStatusesItem,
)
from ...models.payment_batch_payments_response import PaymentBatchPaymentsResponse
from ...models.payment_payment_statuses_item import PaymentPaymentStatusesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    external_reference: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    batch_payment_statuses: Union[Unset, None, List[PaymentBatchPaymentStatusesItem]] = UNSET,
    payment_statuses: Union[Unset, None, List[PaymentPaymentStatusesItem]] = UNSET,
    approval_status: Union[Unset, None, List[PaymentApprovalStatusItem]] = UNSET,
    current_user_can_approve: Union[Unset, None, str] = UNSET,
    created_by_customer_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = "20",
) -> Dict[str, Any]:
    url = f"{client.base_url}/batchpayments"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["externalReference"] = external_reference

    params["fromCreatedDate"] = from_created_date

    json_batch_payment_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(batch_payment_statuses, Unset):
        if batch_payment_statuses is None:
            json_batch_payment_statuses = None
        else:
            json_batch_payment_statuses = []
            for (
                componentsschemaspayment_batch_payment_statuses_item_data
            ) in batch_payment_statuses:
                componentsschemaspayment_batch_payment_statuses_item = (
                    componentsschemaspayment_batch_payment_statuses_item_data.value
                )

                json_batch_payment_statuses.append(
                    componentsschemaspayment_batch_payment_statuses_item
                )

    params["batchPaymentStatuses"] = json_batch_payment_statuses

    json_payment_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(payment_statuses, Unset):
        if payment_statuses is None:
            json_payment_statuses = None
        else:
            json_payment_statuses = []
            for componentsschemaspayment_payment_statuses_item_data in payment_statuses:
                componentsschemaspayment_payment_statuses_item = (
                    componentsschemaspayment_payment_statuses_item_data.value
                )

                json_payment_statuses.append(componentsschemaspayment_payment_statuses_item)

    params["paymentStatuses"] = json_payment_statuses

    json_approval_status: Union[Unset, None, List[str]] = UNSET
    if not isinstance(approval_status, Unset):
        if approval_status is None:
            json_approval_status = None
        else:
            json_approval_status = []
            for componentsschemaspayment_approval_status_item_data in approval_status:
                componentsschemaspayment_approval_status_item = (
                    componentsschemaspayment_approval_status_item_data.value
                )

                json_approval_status.append(componentsschemaspayment_approval_status_item)

    params["approvalStatus"] = json_approval_status

    params["currentUserCanApprove"] = current_user_can_approve

    params["createdByCustomerId"] = created_by_customer_id

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
) -> Optional[PaymentBatchPaymentsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaymentBatchPaymentsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PaymentBatchPaymentsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    external_reference: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    batch_payment_statuses: Union[Unset, None, List[PaymentBatchPaymentStatusesItem]] = UNSET,
    payment_statuses: Union[Unset, None, List[PaymentPaymentStatusesItem]] = UNSET,
    approval_status: Union[Unset, None, List[PaymentApprovalStatusItem]] = UNSET,
    current_user_can_approve: Union[Unset, None, str] = UNSET,
    created_by_customer_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = "20",
) -> Response[PaymentBatchPaymentsResponse]:
    """Get batch payments by a given set of parameters

     This endpoint allows for a user who has submitted multiple batch to use some criteria to get the
    batch payments.

    Args:
        external_reference (Union[Unset, None, str]): Batch payments External Reference contains
            this text. Example: aReference_00001.
        from_created_date (Union[Unset, None, str]): Batch payments created date equal or after to
            this date. Example: 2022-05-16.
        batch_payment_statuses (Union[Unset, None, List[PaymentBatchPaymentStatusesItem]]):
        payment_statuses (Union[Unset, None, List[PaymentPaymentStatusesItem]]):
        approval_status (Union[Unset, None, List[PaymentApprovalStatusItem]]):
        current_user_can_approve (Union[Unset, None, str]): Only return batch payments the current
            user can approve. Example: true.
        created_by_customer_id (Union[Unset, None, str]): Limit results by the customer which
            created the batch payment request
        page (Union[Unset, None, str]): Page to fetch (0 indexed) Default: '0'.
        size (Union[Unset, None, str]): Size of Page to fetch Default: '20'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        external_reference=external_reference,
        from_created_date=from_created_date,
        batch_payment_statuses=batch_payment_statuses,
        payment_statuses=payment_statuses,
        approval_status=approval_status,
        current_user_can_approve=current_user_can_approve,
        created_by_customer_id=created_by_customer_id,
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
    external_reference: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    batch_payment_statuses: Union[Unset, None, List[PaymentBatchPaymentStatusesItem]] = UNSET,
    payment_statuses: Union[Unset, None, List[PaymentPaymentStatusesItem]] = UNSET,
    approval_status: Union[Unset, None, List[PaymentApprovalStatusItem]] = UNSET,
    current_user_can_approve: Union[Unset, None, str] = UNSET,
    created_by_customer_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = "20",
) -> Optional[PaymentBatchPaymentsResponse]:
    """Get batch payments by a given set of parameters

     This endpoint allows for a user who has submitted multiple batch to use some criteria to get the
    batch payments.

    Args:
        external_reference (Union[Unset, None, str]): Batch payments External Reference contains
            this text. Example: aReference_00001.
        from_created_date (Union[Unset, None, str]): Batch payments created date equal or after to
            this date. Example: 2022-05-16.
        batch_payment_statuses (Union[Unset, None, List[PaymentBatchPaymentStatusesItem]]):
        payment_statuses (Union[Unset, None, List[PaymentPaymentStatusesItem]]):
        approval_status (Union[Unset, None, List[PaymentApprovalStatusItem]]):
        current_user_can_approve (Union[Unset, None, str]): Only return batch payments the current
            user can approve. Example: true.
        created_by_customer_id (Union[Unset, None, str]): Limit results by the customer which
            created the batch payment request
        page (Union[Unset, None, str]): Page to fetch (0 indexed) Default: '0'.
        size (Union[Unset, None, str]): Size of Page to fetch Default: '20'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentsResponse]
    """

    return sync_detailed(
        client=client,
        external_reference=external_reference,
        from_created_date=from_created_date,
        batch_payment_statuses=batch_payment_statuses,
        payment_statuses=payment_statuses,
        approval_status=approval_status,
        current_user_can_approve=current_user_can_approve,
        created_by_customer_id=created_by_customer_id,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    external_reference: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    batch_payment_statuses: Union[Unset, None, List[PaymentBatchPaymentStatusesItem]] = UNSET,
    payment_statuses: Union[Unset, None, List[PaymentPaymentStatusesItem]] = UNSET,
    approval_status: Union[Unset, None, List[PaymentApprovalStatusItem]] = UNSET,
    current_user_can_approve: Union[Unset, None, str] = UNSET,
    created_by_customer_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = "20",
) -> Response[PaymentBatchPaymentsResponse]:
    """Get batch payments by a given set of parameters

     This endpoint allows for a user who has submitted multiple batch to use some criteria to get the
    batch payments.

    Args:
        external_reference (Union[Unset, None, str]): Batch payments External Reference contains
            this text. Example: aReference_00001.
        from_created_date (Union[Unset, None, str]): Batch payments created date equal or after to
            this date. Example: 2022-05-16.
        batch_payment_statuses (Union[Unset, None, List[PaymentBatchPaymentStatusesItem]]):
        payment_statuses (Union[Unset, None, List[PaymentPaymentStatusesItem]]):
        approval_status (Union[Unset, None, List[PaymentApprovalStatusItem]]):
        current_user_can_approve (Union[Unset, None, str]): Only return batch payments the current
            user can approve. Example: true.
        created_by_customer_id (Union[Unset, None, str]): Limit results by the customer which
            created the batch payment request
        page (Union[Unset, None, str]): Page to fetch (0 indexed) Default: '0'.
        size (Union[Unset, None, str]): Size of Page to fetch Default: '20'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        external_reference=external_reference,
        from_created_date=from_created_date,
        batch_payment_statuses=batch_payment_statuses,
        payment_statuses=payment_statuses,
        approval_status=approval_status,
        current_user_can_approve=current_user_can_approve,
        created_by_customer_id=created_by_customer_id,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    external_reference: Union[Unset, None, str] = UNSET,
    from_created_date: Union[Unset, None, str] = UNSET,
    batch_payment_statuses: Union[Unset, None, List[PaymentBatchPaymentStatusesItem]] = UNSET,
    payment_statuses: Union[Unset, None, List[PaymentPaymentStatusesItem]] = UNSET,
    approval_status: Union[Unset, None, List[PaymentApprovalStatusItem]] = UNSET,
    current_user_can_approve: Union[Unset, None, str] = UNSET,
    created_by_customer_id: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, str] = "0",
    size: Union[Unset, None, str] = "20",
) -> Optional[PaymentBatchPaymentsResponse]:
    """Get batch payments by a given set of parameters

     This endpoint allows for a user who has submitted multiple batch to use some criteria to get the
    batch payments.

    Args:
        external_reference (Union[Unset, None, str]): Batch payments External Reference contains
            this text. Example: aReference_00001.
        from_created_date (Union[Unset, None, str]): Batch payments created date equal or after to
            this date. Example: 2022-05-16.
        batch_payment_statuses (Union[Unset, None, List[PaymentBatchPaymentStatusesItem]]):
        payment_statuses (Union[Unset, None, List[PaymentPaymentStatusesItem]]):
        approval_status (Union[Unset, None, List[PaymentApprovalStatusItem]]):
        current_user_can_approve (Union[Unset, None, str]): Only return batch payments the current
            user can approve. Example: true.
        created_by_customer_id (Union[Unset, None, str]): Limit results by the customer which
            created the batch payment request
        page (Union[Unset, None, str]): Page to fetch (0 indexed) Default: '0'.
        size (Union[Unset, None, str]): Size of Page to fetch Default: '20'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaymentBatchPaymentsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            external_reference=external_reference,
            from_created_date=from_created_date,
            batch_payment_statuses=batch_payment_statuses,
            payment_statuses=payment_statuses,
            approval_status=approval_status,
            current_user_can_approve=current_user_can_approve,
            created_by_customer_id=created_by_customer_id,
            page=page,
            size=size,
        )
    ).parsed
