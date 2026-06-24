from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_store import PaginatedResponseStore
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_after: None | str | Unset
    if isinstance(after, Unset):
        json_after = UNSET
    else:
        json_after = after
    params["after"] = json_after

    json_before: None | str | Unset
    if isinstance(before, Unset):
        json_before = UNSET
    else:
        json_before = before
    params["before"] = json_before

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/stores/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponseStore | None:
    if response.status_code == 200:
        response_200 = PaginatedResponseStore.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | PaginatedResponseStore]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | PaginatedResponseStore]:
    """List Stores

     Retrieve a list of all stores in the system.

    Args:
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseStore]
    """

    kwargs = _get_kwargs(
        after=after,
        before=before,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
) -> HTTPValidationError | PaginatedResponseStore | None:
    """List Stores

     Retrieve a list of all stores in the system.

    Args:
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseStore
    """

    return sync_detailed(
        client=client,
        after=after,
        before=before,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | PaginatedResponseStore]:
    """List Stores

     Retrieve a list of all stores in the system.

    Args:
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseStore]
    """

    kwargs = _get_kwargs(
        after=after,
        before=before,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
) -> HTTPValidationError | PaginatedResponseStore | None:
    """List Stores

     Retrieve a list of all stores in the system.

    Args:
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseStore
    """

    return (
        await asyncio_detailed(
            client=client,
            after=after,
            before=before,
            limit=limit,
        )
    ).parsed
