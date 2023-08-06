from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.account_customer import AccountCustomer
from ...models.get_customer_statuses_item import GetCustomerStatusesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    customer_id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetCustomerStatusesItem]] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers/{customer_id}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_statuses: Union[Unset, None, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        if statuses is None:
            json_statuses = None
        else:
            json_statuses = []
            for statuses_item_data in statuses:
                statuses_item = statuses_item_data.value

                json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

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
    statuses: Union[Unset, None, List[GetCustomerStatusesItem]] = UNSET,
) -> Response[AccountCustomer]:
    """Retrieve a specific customer using a unique customer reference

     Retrieve a specific customer using a unique customer reference. This identifier can be found in the
    response obtained after creating a new customer, it starts by C, e.g: C0000000

    Args:
        customer_id (str):
        statuses (Union[Unset, None, List[GetCustomerStatusesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        statuses=statuses,
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
    statuses: Union[Unset, None, List[GetCustomerStatusesItem]] = UNSET,
) -> Optional[AccountCustomer]:
    """Retrieve a specific customer using a unique customer reference

     Retrieve a specific customer using a unique customer reference. This identifier can be found in the
    response obtained after creating a new customer, it starts by C, e.g: C0000000

    Args:
        customer_id (str):
        statuses (Union[Unset, None, List[GetCustomerStatusesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
    """

    return sync_detailed(
        customer_id=customer_id,
        client=client,
        statuses=statuses,
    ).parsed


async def asyncio_detailed(
    customer_id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetCustomerStatusesItem]] = UNSET,
) -> Response[AccountCustomer]:
    """Retrieve a specific customer using a unique customer reference

     Retrieve a specific customer using a unique customer reference. This identifier can be found in the
    response obtained after creating a new customer, it starts by C, e.g: C0000000

    Args:
        customer_id (str):
        statuses (Union[Unset, None, List[GetCustomerStatusesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountCustomer]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
        client=client,
        statuses=statuses,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    customer_id: str,
    *,
    client: Client,
    statuses: Union[Unset, None, List[GetCustomerStatusesItem]] = UNSET,
) -> Optional[AccountCustomer]:
    """Retrieve a specific customer using a unique customer reference

     Retrieve a specific customer using a unique customer reference. This identifier can be found in the
    response obtained after creating a new customer, it starts by C, e.g: C0000000

    Args:
        customer_id (str):
        statuses (Union[Unset, None, List[GetCustomerStatusesItem]]):

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
            statuses=statuses,
        )
    ).parsed
