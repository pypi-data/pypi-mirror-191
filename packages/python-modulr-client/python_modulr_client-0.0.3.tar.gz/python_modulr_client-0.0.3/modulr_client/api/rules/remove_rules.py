from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.remove_rules_response_200 import RemoveRulesResponse200
from ...models.remove_rules_response_207 import RemoveRulesResponse207
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    r_ids: List[str],
) -> Dict[str, Any]:
    url = f"{client.base_url}/rules"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_r_ids = r_ids

    params["rIds"] = json_r_ids

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
) -> Optional[Union[RemoveRulesResponse200, RemoveRulesResponse207]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RemoveRulesResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.MULTI_STATUS:
        response_207 = RemoveRulesResponse207.from_dict(response.json())

        return response_207
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    r_ids: List[str],
) -> Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]:
    """Delete a Rule

     When you no longer want a rule on an account you can do it with this endpoint. You can delete more
    than one rule in the same request.

    Args:
        r_ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]
    """

    kwargs = _get_kwargs(
        client=client,
        r_ids=r_ids,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    r_ids: List[str],
) -> Optional[Union[RemoveRulesResponse200, RemoveRulesResponse207]]:
    """Delete a Rule

     When you no longer want a rule on an account you can do it with this endpoint. You can delete more
    than one rule in the same request.

    Args:
        r_ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]
    """

    return sync_detailed(
        client=client,
        r_ids=r_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    r_ids: List[str],
) -> Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]:
    """Delete a Rule

     When you no longer want a rule on an account you can do it with this endpoint. You can delete more
    than one rule in the same request.

    Args:
        r_ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]
    """

    kwargs = _get_kwargs(
        client=client,
        r_ids=r_ids,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    r_ids: List[str],
) -> Optional[Union[RemoveRulesResponse200, RemoveRulesResponse207]]:
    """Delete a Rule

     When you no longer want a rule on an account you can do it with this endpoint. You can delete more
    than one rule in the same request.

    Args:
        r_ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RemoveRulesResponse200, RemoveRulesResponse207]]
    """

    return (
        await asyncio_detailed(
            client=client,
            r_ids=r_ids,
        )
    ).parsed
