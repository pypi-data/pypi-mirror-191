from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.account_customer import AccountCustomer
from ...models.account_update_customer_request import AccountUpdateCustomerRequest
from ...types import Response


def _get_kwargs(
    customer_id: str,
    *,
    client: Client,
    json_body: AccountUpdateCustomerRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers/{customer_id}"

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[AccountCustomer]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountCustomer.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[AccountCustomer]:
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
    json_body: AccountUpdateCustomerRequest,
) -> Response[AccountCustomer]:
    """Edit a specific customer using a unique customer reference

     This identifier can be found in the response obtained after creating a new customer, it starts by C,
    e.g:C0000000
    Currently editable fields:
    1. for all customer types, externalReference can be edited
    2. for PCM_BUSINESS customer type, name and tradingAddress can additionally be edited
    3. for PCM_INDIVIDUAL customer type, the associate can additionally be edited

    Args:
        customer_id (str):
        json_body (AccountUpdateCustomerRequest): Details of customer to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
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
    json_body: AccountUpdateCustomerRequest,
) -> Optional[AccountCustomer]:
    """Edit a specific customer using a unique customer reference

     This identifier can be found in the response obtained after creating a new customer, it starts by C,
    e.g:C0000000
    Currently editable fields:
    1. for all customer types, externalReference can be edited
    2. for PCM_BUSINESS customer type, name and tradingAddress can additionally be edited
    3. for PCM_INDIVIDUAL customer type, the associate can additionally be edited

    Args:
        customer_id (str):
        json_body (AccountUpdateCustomerRequest): Details of customer to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
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
    json_body: AccountUpdateCustomerRequest,
) -> Response[AccountCustomer]:
    """Edit a specific customer using a unique customer reference

     This identifier can be found in the response obtained after creating a new customer, it starts by C,
    e.g:C0000000
    Currently editable fields:
    1. for all customer types, externalReference can be edited
    2. for PCM_BUSINESS customer type, name and tradingAddress can additionally be edited
    3. for PCM_INDIVIDUAL customer type, the associate can additionally be edited

    Args:
        customer_id (str):
        json_body (AccountUpdateCustomerRequest): Details of customer to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
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
    json_body: AccountUpdateCustomerRequest,
) -> Optional[AccountCustomer]:
    """Edit a specific customer using a unique customer reference

     This identifier can be found in the response obtained after creating a new customer, it starts by C,
    e.g:C0000000
    Currently editable fields:
    1. for all customer types, externalReference can be edited
    2. for PCM_BUSINESS customer type, name and tradingAddress can additionally be edited
    3. for PCM_INDIVIDUAL customer type, the associate can additionally be edited

    Args:
        customer_id (str):
        json_body (AccountUpdateCustomerRequest): Details of customer to edit

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
    """

    return (
        await asyncio_detailed(
            customer_id=customer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
