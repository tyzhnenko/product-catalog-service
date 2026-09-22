from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_category import PaginatedResponseCategory
from ...models.paginated_response_partial_category import PaginatedResponsePartialCategory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    *,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    fields: None | str | Unset = UNSET,
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

    json_fields: None | str | Unset
    if isinstance(fields, Unset):
        json_fields = UNSET
    else:
        json_fields = fields
    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/categories/{store_id}".format(
            store_id=quote(str(store_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> PaginatedResponseCategory | PaginatedResponsePartialCategory:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = PaginatedResponseCategory.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = PaginatedResponsePartialCategory.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory]:
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
    fields: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory]:
    """List Categories

     Retrieve a list of all categories for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        fields=fields,
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
    fields: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory | None:
    """List Categories

     Retrieve a list of all categories for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    fields: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory]:
    """List Categories

     Retrieve a list of all categories for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        fields=fields,
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
    fields: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory | None:
    """List Categories

     Retrieve a list of all categories for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseCategory | PaginatedResponsePartialCategory
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            after=after,
            before=before,
            limit=limit,
            attrs=attrs,
            fields=fields,
        )
    ).parsed
