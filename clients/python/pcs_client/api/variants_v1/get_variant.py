from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.partial_product_variant import PartialProductVariant
from ...models.product_variant import ProductVariant
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    fields: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_fields: None | str | Unset
    if isinstance(fields, Unset):
        json_fields = UNSET
    else:
        json_fields = fields
    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/variants/{store_id}/{product_id}/{variant_id}".format(
            store_id=quote(str(store_id), safe=""),
            product_id=quote(str(product_id), safe=""),
            variant_id=quote(str(variant_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PartialProductVariant | ProductVariant | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> PartialProductVariant | ProductVariant:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = ProductVariant.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = PartialProductVariant.from_dict(data)

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
) -> Response[HTTPValidationError | PartialProductVariant | ProductVariant]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    client: AuthenticatedClient,
    fields: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PartialProductVariant | ProductVariant]:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        variant_id (str): Variant ID or slug ref (prefixed 's-')
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
        Response[HTTPValidationError | PartialProductVariant | ProductVariant]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        variant_id=variant_id,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    client: AuthenticatedClient,
    fields: None | str | Unset = UNSET,
) -> HTTPValidationError | PartialProductVariant | ProductVariant | None:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        variant_id (str): Variant ID or slug ref (prefixed 's-')
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
        HTTPValidationError | PartialProductVariant | ProductVariant
    """

    return sync_detailed(
        store_id=store_id,
        product_id=product_id,
        variant_id=variant_id,
        client=client,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    client: AuthenticatedClient,
    fields: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PartialProductVariant | ProductVariant]:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        variant_id (str): Variant ID or slug ref (prefixed 's-')
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
        Response[HTTPValidationError | PartialProductVariant | ProductVariant]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        variant_id=variant_id,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    client: AuthenticatedClient,
    fields: None | str | Unset = UNSET,
) -> HTTPValidationError | PartialProductVariant | ProductVariant | None:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        variant_id (str): Variant ID or slug ref (prefixed 's-')
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
        HTTPValidationError | PartialProductVariant | ProductVariant
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            product_id=product_id,
            variant_id=variant_id,
            client=client,
            fields=fields,
        )
    ).parsed
