from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_product import PaginatedResponseProduct
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    *,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
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

    json_attrs: list[str] | Unset = UNSET
    if not isinstance(attrs, Unset):
        json_attrs = attrs

    params["attrs"] = json_attrs

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/products/{store_id}".format(
            store_id=quote(str(store_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponseProduct | None:
    if response.status_code == 200:
        response_200 = PaginatedResponseProduct.from_dict(response.json())

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
) -> Response[HTTPValidationError | PaginatedResponseProduct]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseProduct]:
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseProduct]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseProduct | None:
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseProduct
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseProduct]:
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseProduct]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseProduct | None:
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseProduct
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            after=after,
            before=before,
            limit=limit,
            attrs=attrs,
        )
    ).parsed
