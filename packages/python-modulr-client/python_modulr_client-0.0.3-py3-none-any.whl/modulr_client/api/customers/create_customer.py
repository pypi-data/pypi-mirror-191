from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.account_create_customer_request import AccountCreateCustomerRequest
from ...models.account_customer import AccountCustomer
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AccountCreateCustomerRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers"

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[AccountCustomer]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = AccountCustomer.from_dict(response.json())

        return response_201
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
    *,
    client: Client,
    json_body: AccountCreateCustomerRequest,
) -> Response[AccountCustomer]:
    """Create a new customer

     This endpoint allows you to create a new customer. Creating a customer is a complex process with
    several dependencies, e.g: Directors, type of customer, legal specifications. For further
    information, please visit 'Creating a customer and account' entry on our API documentation

    Args:
        json_body (AccountCreateCustomerRequest): Details of customer to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
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
    json_body: AccountCreateCustomerRequest,
) -> Optional[AccountCustomer]:
    """Create a new customer

     This endpoint allows you to create a new customer. Creating a customer is a complex process with
    several dependencies, e.g: Directors, type of customer, legal specifications. For further
    information, please visit 'Creating a customer and account' entry on our API documentation

    Args:
        json_body (AccountCreateCustomerRequest): Details of customer to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: AccountCreateCustomerRequest,
) -> Response[AccountCustomer]:
    """Create a new customer

     This endpoint allows you to create a new customer. Creating a customer is a complex process with
    several dependencies, e.g: Directors, type of customer, legal specifications. For further
    information, please visit 'Creating a customer and account' entry on our API documentation

    Args:
        json_body (AccountCreateCustomerRequest): Details of customer to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
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
    json_body: AccountCreateCustomerRequest,
) -> Optional[AccountCustomer]:
    """Create a new customer

     This endpoint allows you to create a new customer. Creating a customer is a complex process with
    several dependencies, e.g: Directors, type of customer, legal specifications. For further
    information, please visit 'Creating a customer and account' entry on our API documentation

    Args:
        json_body (AccountCreateCustomerRequest): Details of customer to create

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
