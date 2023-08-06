from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    account_id: str,
    mandate_id: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, str] = UNSET,
    end_date: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/collections"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["accountId"] = account_id

    params["mandateId"] = mandate_id

    params["type"] = type

    params["startDate"] = start_date

    params["endDate"] = end_date

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    account_id: str,
    mandate_id: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, str] = UNSET,
    end_date: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get all collection activities of an account

     Once a collection schedule has been set up any collections that have happened (successful or not)
    can be viewed. There is no pagination (although the enclosing response structure indicates
    pagination); 'page' value will always be zero.

    Args:
        account_id (str):
        mandate_id (Union[Unset, None, str]):
        type (Union[Unset, None, str]):
        start_date (Union[Unset, None, str]):
        end_date (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
        mandate_id=mandate_id,
        type=type,
        start_date=start_date,
        end_date=end_date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Client,
    account_id: str,
    mandate_id: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, str] = UNSET,
    end_date: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get all collection activities of an account

     Once a collection schedule has been set up any collections that have happened (successful or not)
    can be viewed. There is no pagination (although the enclosing response structure indicates
    pagination); 'page' value will always be zero.

    Args:
        account_id (str):
        mandate_id (Union[Unset, None, str]):
        type (Union[Unset, None, str]):
        start_date (Union[Unset, None, str]):
        end_date (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
        mandate_id=mandate_id,
        type=type,
        start_date=start_date,
        end_date=end_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
