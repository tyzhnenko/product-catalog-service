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
    price_key: None | str | Unset = UNSET,
    price_min: float | None | str | Unset = UNSET,
    price_max: float | None | str | Unset = UNSET,
    location_price_id: None | str | Unset = UNSET,
    location_price_key: None | str | Unset = UNSET,
    location_price_min: float | None | str | Unset = UNSET,
    location_price_max: float | None | str | Unset = UNSET,
    region_price_code: None | str | Unset = UNSET,
    region_price_key: None | str | Unset = UNSET,
    region_price_min: float | None | str | Unset = UNSET,
    region_price_max: float | None | str | Unset = UNSET,
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

    json_price_key: None | str | Unset
    if isinstance(price_key, Unset):
        json_price_key = UNSET
    else:
        json_price_key = price_key
    params["price_key"] = json_price_key

    json_price_min: float | None | str | Unset
    if isinstance(price_min, Unset):
        json_price_min = UNSET
    else:
        json_price_min = price_min
    params["price_min"] = json_price_min

    json_price_max: float | None | str | Unset
    if isinstance(price_max, Unset):
        json_price_max = UNSET
    else:
        json_price_max = price_max
    params["price_max"] = json_price_max

    json_location_price_id: None | str | Unset
    if isinstance(location_price_id, Unset):
        json_location_price_id = UNSET
    else:
        json_location_price_id = location_price_id
    params["location_price_id"] = json_location_price_id

    json_location_price_key: None | str | Unset
    if isinstance(location_price_key, Unset):
        json_location_price_key = UNSET
    else:
        json_location_price_key = location_price_key
    params["location_price_key"] = json_location_price_key

    json_location_price_min: float | None | str | Unset
    if isinstance(location_price_min, Unset):
        json_location_price_min = UNSET
    else:
        json_location_price_min = location_price_min
    params["location_price_min"] = json_location_price_min

    json_location_price_max: float | None | str | Unset
    if isinstance(location_price_max, Unset):
        json_location_price_max = UNSET
    else:
        json_location_price_max = location_price_max
    params["location_price_max"] = json_location_price_max

    json_region_price_code: None | str | Unset
    if isinstance(region_price_code, Unset):
        json_region_price_code = UNSET
    else:
        json_region_price_code = region_price_code
    params["region_price_code"] = json_region_price_code

    json_region_price_key: None | str | Unset
    if isinstance(region_price_key, Unset):
        json_region_price_key = UNSET
    else:
        json_region_price_key = region_price_key
    params["region_price_key"] = json_region_price_key

    json_region_price_min: float | None | str | Unset
    if isinstance(region_price_min, Unset):
        json_region_price_min = UNSET
    else:
        json_region_price_min = region_price_min
    params["region_price_min"] = json_region_price_min

    json_region_price_max: float | None | str | Unset
    if isinstance(region_price_max, Unset):
        json_region_price_max = UNSET
    else:
        json_region_price_max = region_price_max
    params["region_price_max"] = json_region_price_max

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
    price_key: None | str | Unset = UNSET,
    price_min: float | None | str | Unset = UNSET,
    price_max: float | None | str | Unset = UNSET,
    location_price_id: None | str | Unset = UNSET,
    location_price_key: None | str | Unset = UNSET,
    location_price_min: float | None | str | Unset = UNSET,
    location_price_max: float | None | str | Unset = UNSET,
    region_price_code: None | str | Unset = UNSET,
    region_price_key: None | str | Unset = UNSET,
    region_price_min: float | None | str | Unset = UNSET,
    region_price_max: float | None | str | Unset = UNSET,
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
        price_key (None | str | Unset): Price map key to filter on (e.g. 'USD')
        price_min (float | None | str | Unset): Minimum price value (inclusive)
        price_max (float | None | str | Unset): Maximum price value (inclusive)
        location_price_id (None | str | Unset): Location ID for location price filtering
        location_price_key (None | str | Unset): Price key within the location price map
        location_price_min (float | None | str | Unset): Minimum location price value (inclusive)
        location_price_max (float | None | str | Unset): Maximum location price value (inclusive)
        region_price_code (None | str | Unset): Region/country code for region price filtering
            (ISO 3166-1 alpha-2)
        region_price_key (None | str | Unset): Price key within the region price map
        region_price_min (float | None | str | Unset): Minimum region price value (inclusive)
        region_price_max (float | None | str | Unset): Maximum region price value (inclusive)

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
        price_key=price_key,
        price_min=price_min,
        price_max=price_max,
        location_price_id=location_price_id,
        location_price_key=location_price_key,
        location_price_min=location_price_min,
        location_price_max=location_price_max,
        region_price_code=region_price_code,
        region_price_key=region_price_key,
        region_price_min=region_price_min,
        region_price_max=region_price_max,
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
    price_key: None | str | Unset = UNSET,
    price_min: float | None | str | Unset = UNSET,
    price_max: float | None | str | Unset = UNSET,
    location_price_id: None | str | Unset = UNSET,
    location_price_key: None | str | Unset = UNSET,
    location_price_min: float | None | str | Unset = UNSET,
    location_price_max: float | None | str | Unset = UNSET,
    region_price_code: None | str | Unset = UNSET,
    region_price_key: None | str | Unset = UNSET,
    region_price_min: float | None | str | Unset = UNSET,
    region_price_max: float | None | str | Unset = UNSET,
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
        price_key (None | str | Unset): Price map key to filter on (e.g. 'USD')
        price_min (float | None | str | Unset): Minimum price value (inclusive)
        price_max (float | None | str | Unset): Maximum price value (inclusive)
        location_price_id (None | str | Unset): Location ID for location price filtering
        location_price_key (None | str | Unset): Price key within the location price map
        location_price_min (float | None | str | Unset): Minimum location price value (inclusive)
        location_price_max (float | None | str | Unset): Maximum location price value (inclusive)
        region_price_code (None | str | Unset): Region/country code for region price filtering
            (ISO 3166-1 alpha-2)
        region_price_key (None | str | Unset): Price key within the region price map
        region_price_min (float | None | str | Unset): Minimum region price value (inclusive)
        region_price_max (float | None | str | Unset): Maximum region price value (inclusive)

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
        price_key=price_key,
        price_min=price_min,
        price_max=price_max,
        location_price_id=location_price_id,
        location_price_key=location_price_key,
        location_price_min=location_price_min,
        location_price_max=location_price_max,
        region_price_code=region_price_code,
        region_price_key=region_price_key,
        region_price_min=region_price_min,
        region_price_max=region_price_max,
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
    price_key: None | str | Unset = UNSET,
    price_min: float | None | str | Unset = UNSET,
    price_max: float | None | str | Unset = UNSET,
    location_price_id: None | str | Unset = UNSET,
    location_price_key: None | str | Unset = UNSET,
    location_price_min: float | None | str | Unset = UNSET,
    location_price_max: float | None | str | Unset = UNSET,
    region_price_code: None | str | Unset = UNSET,
    region_price_key: None | str | Unset = UNSET,
    region_price_min: float | None | str | Unset = UNSET,
    region_price_max: float | None | str | Unset = UNSET,
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
        price_key (None | str | Unset): Price map key to filter on (e.g. 'USD')
        price_min (float | None | str | Unset): Minimum price value (inclusive)
        price_max (float | None | str | Unset): Maximum price value (inclusive)
        location_price_id (None | str | Unset): Location ID for location price filtering
        location_price_key (None | str | Unset): Price key within the location price map
        location_price_min (float | None | str | Unset): Minimum location price value (inclusive)
        location_price_max (float | None | str | Unset): Maximum location price value (inclusive)
        region_price_code (None | str | Unset): Region/country code for region price filtering
            (ISO 3166-1 alpha-2)
        region_price_key (None | str | Unset): Price key within the region price map
        region_price_min (float | None | str | Unset): Minimum region price value (inclusive)
        region_price_max (float | None | str | Unset): Maximum region price value (inclusive)

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
        price_key=price_key,
        price_min=price_min,
        price_max=price_max,
        location_price_id=location_price_id,
        location_price_key=location_price_key,
        location_price_min=location_price_min,
        location_price_max=location_price_max,
        region_price_code=region_price_code,
        region_price_key=region_price_key,
        region_price_min=region_price_min,
        region_price_max=region_price_max,
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
    price_key: None | str | Unset = UNSET,
    price_min: float | None | str | Unset = UNSET,
    price_max: float | None | str | Unset = UNSET,
    location_price_id: None | str | Unset = UNSET,
    location_price_key: None | str | Unset = UNSET,
    location_price_min: float | None | str | Unset = UNSET,
    location_price_max: float | None | str | Unset = UNSET,
    region_price_code: None | str | Unset = UNSET,
    region_price_key: None | str | Unset = UNSET,
    region_price_min: float | None | str | Unset = UNSET,
    region_price_max: float | None | str | Unset = UNSET,
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
        price_key (None | str | Unset): Price map key to filter on (e.g. 'USD')
        price_min (float | None | str | Unset): Minimum price value (inclusive)
        price_max (float | None | str | Unset): Maximum price value (inclusive)
        location_price_id (None | str | Unset): Location ID for location price filtering
        location_price_key (None | str | Unset): Price key within the location price map
        location_price_min (float | None | str | Unset): Minimum location price value (inclusive)
        location_price_max (float | None | str | Unset): Maximum location price value (inclusive)
        region_price_code (None | str | Unset): Region/country code for region price filtering
            (ISO 3166-1 alpha-2)
        region_price_key (None | str | Unset): Price key within the region price map
        region_price_min (float | None | str | Unset): Minimum region price value (inclusive)
        region_price_max (float | None | str | Unset): Maximum region price value (inclusive)

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
            price_key=price_key,
            price_min=price_min,
            price_max=price_max,
            location_price_id=location_price_id,
            location_price_key=location_price_key,
            location_price_min=location_price_min,
            location_price_max=location_price_max,
            region_price_code=region_price_code,
            region_price_key=region_price_key,
            region_price_min=region_price_min,
            region_price_max=region_price_max,
        )
    ).parsed
