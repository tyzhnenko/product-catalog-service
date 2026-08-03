from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_product_variant import PaginatedResponseProductVariant
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    product_id: str,
    *,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
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

    json_price: None | str | Unset
    if isinstance(price, Unset):
        json_price = UNSET
    else:
        json_price = price
    params["price"] = json_price

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/variants/{store_id}/{product_id}".format(
            store_id=quote(str(store_id), safe=""),
            product_id=quote(str(product_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponseProductVariant | None:
    if response.status_code == 200:
        response_200 = PaginatedResponseProductVariant.from_dict(response.json())

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
) -> Response[HTTPValidationError | PaginatedResponseProductVariant]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    product_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseProductVariant]:
    """List Variants

     Retrieve a list of all variants for a specific product.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        price (None | str | Unset): Whitespace-separated price search tokens (shlex-quoted for
            values containing spaces). '<key>>=<value>' / '<key><=<value>' filter the top-level price
            map. 'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-
            only checks any key is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseProductVariant]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        price=price,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    product_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseProductVariant | None:
    """List Variants

     Retrieve a list of all variants for a specific product.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        price (None | str | Unset): Whitespace-separated price search tokens (shlex-quoted for
            values containing spaces). '<key>>=<value>' / '<key><=<value>' filter the top-level price
            map. 'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-
            only checks any key is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseProductVariant
    """

    return sync_detailed(
        store_id=store_id,
        product_id=product_id,
        client=client,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        price=price,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    product_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseProductVariant]:
    """List Variants

     Retrieve a list of all variants for a specific product.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        price (None | str | Unset): Whitespace-separated price search tokens (shlex-quoted for
            values containing spaces). '<key>>=<value>' / '<key><=<value>' filter the top-level price
            map. 'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-
            only checks any key is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseProductVariant]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        price=price,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    product_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseProductVariant | None:
    """List Variants

     Retrieve a list of all variants for a specific product.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Attribute filters in 'key:value' format. Repeat for multiple
            values. Same key = OR, different keys = AND.
        price (None | str | Unset): Whitespace-separated price search tokens (shlex-quoted for
            values containing spaces). '<key>>=<value>' / '<key><=<value>' filter the top-level price
            map. 'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-
            only checks any key is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseProductVariant
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            product_id=product_id,
            client=client,
            after=after,
            before=before,
            limit=limit,
            attrs=attrs,
            price=price,
        )
    ).parsed
