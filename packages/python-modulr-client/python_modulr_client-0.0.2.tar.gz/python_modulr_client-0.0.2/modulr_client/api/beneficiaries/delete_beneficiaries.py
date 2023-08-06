from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.delete_beneficiaries_response_200 import DeleteBeneficiariesResponse200
from ...types import UNSET, Response


def _get_kwargs(
    cid: str,
    *,
    client: Client,
    bid: List[str],
) -> Dict[str, Any]:
    url = f"{client.base_url}/customers/{cid}/beneficiaries"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_bid = bid

    params["bid"] = json_bid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[DeleteBeneficiariesResponse200, str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteBeneficiariesResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.MULTI_STATUS:
        response_207 = cast(str, response.json())
        return response_207
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DeleteBeneficiariesResponse200, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cid: str,
    *,
    client: Client,
    bid: List[str],
) -> Response[Union[DeleteBeneficiariesResponse200, str]]:
    """Delete beneficiaries for a specified customer

     deleting beneficiaries for a customer, using their customer ID

    Args:
        cid (str):
        bid (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteBeneficiariesResponse200, str]]
    """

    kwargs = _get_kwargs(
        cid=cid,
        client=client,
        bid=bid,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cid: str,
    *,
    client: Client,
    bid: List[str],
) -> Optional[Union[DeleteBeneficiariesResponse200, str]]:
    """Delete beneficiaries for a specified customer

     deleting beneficiaries for a customer, using their customer ID

    Args:
        cid (str):
        bid (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteBeneficiariesResponse200, str]]
    """

    return sync_detailed(
        cid=cid,
        client=client,
        bid=bid,
    ).parsed


async def asyncio_detailed(
    cid: str,
    *,
    client: Client,
    bid: List[str],
) -> Response[Union[DeleteBeneficiariesResponse200, str]]:
    """Delete beneficiaries for a specified customer

     deleting beneficiaries for a customer, using their customer ID

    Args:
        cid (str):
        bid (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteBeneficiariesResponse200, str]]
    """

    kwargs = _get_kwargs(
        cid=cid,
        client=client,
        bid=bid,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cid: str,
    *,
    client: Client,
    bid: List[str],
) -> Optional[Union[DeleteBeneficiariesResponse200, str]]:
    """Delete beneficiaries for a specified customer

     deleting beneficiaries for a customer, using their customer ID

    Args:
        cid (str):
        bid (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteBeneficiariesResponse200, str]]
    """

    return (
        await asyncio_detailed(
            cid=cid,
            client=client,
            bid=bid,
        )
    ).parsed
