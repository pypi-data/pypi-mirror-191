from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: Union[Unset, None, List[str]] = UNSET,
    account_id: Union[Unset, None, List[str]] = UNSET,
    q: Union[Unset, None, str] = "",
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    from_submitted_date: Union[Unset, None, str] = UNSET,
    to_submitted_date: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[str]] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    reference: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Dict[str, Any]:
    url = f"{client.base_url}/mandates"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_id: Union[Unset, None, List[str]] = UNSET
    if not isinstance(id, Unset):
        if id is None:
            json_id = None
        else:
            json_id = id

    params["id"] = json_id

    json_account_id: Union[Unset, None, List[str]] = UNSET
    if not isinstance(account_id, Unset):
        if account_id is None:
            json_account_id = None
        else:
            json_account_id = account_id

    params["accountId"] = json_account_id

    params["q"] = q

    params["fromCreatedDate"] = from_created_date

    params["toCreatedDate"] = to_created_date

    params["fromSubmittedDate"] = from_submitted_date

    params["toSubmittedDate"] = to_submitted_date

    json_status: Union[Unset, None, List[str]] = UNSET
    if not isinstance(status, Unset):
        if status is None:
            json_status = None
        else:
            json_status = status

    params["status"] = json_status

    params["name"] = name

    params["reference"] = reference

    params["externalReference"] = external_reference

    params["sortField"] = sort_field

    params["sortOrder"] = sort_order

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
    id: Union[Unset, None, List[str]] = UNSET,
    account_id: Union[Unset, None, List[str]] = UNSET,
    q: Union[Unset, None, str] = "",
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    from_submitted_date: Union[Unset, None, str] = UNSET,
    to_submitted_date: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[str]] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    reference: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[Any]:
    """Get Mandates based on search criteria.

     If trying to find one or several particular mandates, then you can narrow down your search by using
    the filters available here. These include the mandate id, either the submitted or created date
    range, the account name on the mandate, etc...

    Args:
        id (Union[Unset, None, List[str]]):
        account_id (Union[Unset, None, List[str]]):
        q (Union[Unset, None, str]):  Default: ''.
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        from_submitted_date (Union[Unset, None, str]):
        to_submitted_date (Union[Unset, None, str]):
        status (Union[Unset, None, List[str]]):
        name (Union[Unset, None, str]):
        reference (Union[Unset, None, str]):
        external_reference (Union[Unset, None, str]):
        sort_field (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        account_id=account_id,
        q=q,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        from_submitted_date=from_submitted_date,
        to_submitted_date=to_submitted_date,
        status=status,
        name=name,
        reference=reference,
        external_reference=external_reference,
        sort_field=sort_field,
        sort_order=sort_order,
        page=page,
        size=size,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Client,
    id: Union[Unset, None, List[str]] = UNSET,
    account_id: Union[Unset, None, List[str]] = UNSET,
    q: Union[Unset, None, str] = "",
    from_created_date: Union[Unset, None, str] = UNSET,
    to_created_date: Union[Unset, None, str] = UNSET,
    from_submitted_date: Union[Unset, None, str] = UNSET,
    to_submitted_date: Union[Unset, None, str] = UNSET,
    status: Union[Unset, None, List[str]] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    reference: Union[Unset, None, str] = UNSET,
    external_reference: Union[Unset, None, str] = UNSET,
    sort_field: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 20,
) -> Response[Any]:
    """Get Mandates based on search criteria.

     If trying to find one or several particular mandates, then you can narrow down your search by using
    the filters available here. These include the mandate id, either the submitted or created date
    range, the account name on the mandate, etc...

    Args:
        id (Union[Unset, None, List[str]]):
        account_id (Union[Unset, None, List[str]]):
        q (Union[Unset, None, str]):  Default: ''.
        from_created_date (Union[Unset, None, str]):
        to_created_date (Union[Unset, None, str]):
        from_submitted_date (Union[Unset, None, str]):
        to_submitted_date (Union[Unset, None, str]):
        status (Union[Unset, None, List[str]]):
        name (Union[Unset, None, str]):
        reference (Union[Unset, None, str]):
        external_reference (Union[Unset, None, str]):
        sort_field (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
        account_id=account_id,
        q=q,
        from_created_date=from_created_date,
        to_created_date=to_created_date,
        from_submitted_date=from_submitted_date,
        to_submitted_date=to_submitted_date,
        status=status,
        name=name,
        reference=reference,
        external_reference=external_reference,
        sort_field=sort_field,
        sort_order=sort_order,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
