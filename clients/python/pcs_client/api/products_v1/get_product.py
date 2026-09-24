from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.partial_product import PartialProduct
from ...models.partial_product_with_variants import PartialProductWithVariants
from ...models.product import Product
from ...models.product_with_variants import ProductWithVariants
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    product_id: str,
    *,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_fields: None | str | Unset
    if isinstance(fields, Unset):
        json_fields = UNSET
    else:
        json_fields = fields
    params["fields"] = json_fields

    json_include: None | str | Unset
    if isinstance(include, Unset):
        json_include = UNSET
    else:
        json_include = include
    params["include"] = json_include

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/products/{store_id}/{product_id}".format(
            store_id=quote(str(store_id), safe=""),
            product_id=quote(str(product_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants | None:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> PartialProduct | PartialProductWithVariants | Product | ProductWithVariants:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = ProductWithVariants.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = PartialProductWithVariants.from_dict(data)

                return response_200_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_2 = Product.from_dict(data)

                return response_200_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_3 = PartialProduct.from_dict(data)

            return response_200_type_3

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
) -> Response[HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants]:
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
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants]:
    """Get Product

     Retrieve a specific product by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.
        include (None | str | Unset): Comma-separated relations to embed in the response.
            Supported: `variants`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        fields=fields,
        include=include,
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
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants | None:
    """Get Product

     Retrieve a specific product by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.
        include (None | str | Unset): Comma-separated relations to embed in the response.
            Supported: `variants`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants
    """

    return sync_detailed(
        store_id=store_id,
        product_id=product_id,
        client=client,
        fields=fields,
        include=include,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    product_id: str,
    *,
    client: AuthenticatedClient,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants]:
    """Get Product

     Retrieve a specific product by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.
        include (None | str | Unset): Comma-separated relations to embed in the response.
            Supported: `variants`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        fields=fields,
        include=include,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    product_id: str,
    *,
    client: AuthenticatedClient,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants | None:
    """Get Product

     Retrieve a specific product by its unique identifier.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        product_id (str): Product ID or slug ref (prefixed 's-')
        fields (None | str | Unset): Comma-separated response fields. Bare names include only
            those fields (`name,brand`); `-` prefixed names exclude them (`-seo,-attributes`). Mixing
            both is not allowed. Dotted paths address nested fields (`seo.slug`,
            `-attributes.roast_level`); keys inside store-defined maps such as `attributes`,
            `location_price` and `region_price` are not validated, since they aren't part of the fixed
            schema. `id` is always returned.
        include (None | str | Unset): Comma-separated relations to embed in the response.
            Supported: `variants`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PartialProduct | PartialProductWithVariants | Product | ProductWithVariants
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            product_id=product_id,
            client=client,
            fields=fields,
            include=include,
        )
    ).parsed
