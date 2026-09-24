from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_partial_product import PaginatedResponsePartialProduct
from ...models.paginated_response_partial_product_with_variants import PaginatedResponsePartialProductWithVariants
from ...models.paginated_response_product import PaginatedResponseProduct
from ...models.paginated_response_product_with_variants import PaginatedResponseProductWithVariants
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    *,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    variants_attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
    variants_availability: None | str | Unset = UNSET,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
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

    json_variants_attrs: list[str] | Unset = UNSET
    if not isinstance(variants_attrs, Unset):
        json_variants_attrs = variants_attrs

    params["variants_attrs"] = json_variants_attrs

    json_price: None | str | Unset
    if isinstance(price, Unset):
        json_price = UNSET
    else:
        json_price = price
    params["price"] = json_price

    json_variants_availability: None | str | Unset
    if isinstance(variants_availability, Unset):
        json_variants_availability = UNSET
    else:
        json_variants_availability = variants_availability
    params["variants_availability"] = json_variants_availability

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
        "url": "/api/v1/products/{store_id}".format(
            store_id=quote(str(store_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    HTTPValidationError
    | PaginatedResponsePartialProduct
    | PaginatedResponsePartialProductWithVariants
    | PaginatedResponseProduct
    | PaginatedResponseProductWithVariants
    | None
):
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> (
            PaginatedResponsePartialProduct
            | PaginatedResponsePartialProductWithVariants
            | PaginatedResponseProduct
            | PaginatedResponseProductWithVariants
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = PaginatedResponseProductWithVariants.from_dict(data)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = PaginatedResponsePartialProductWithVariants.from_dict(data)

                return response_200_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_2 = PaginatedResponseProduct.from_dict(data)

                return response_200_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_3 = PaginatedResponsePartialProduct.from_dict(data)

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
) -> Response[
    HTTPValidationError
    | PaginatedResponsePartialProduct
    | PaginatedResponsePartialProductWithVariants
    | PaginatedResponseProduct
    | PaginatedResponseProductWithVariants
]:
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
    variants_attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
    variants_availability: None | str | Unset = UNSET,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> Response[
    HTTPValidationError
    | PaginatedResponsePartialProduct
    | PaginatedResponsePartialProductWithVariants
    | PaginatedResponseProduct
    | PaginatedResponseProductWithVariants
]:
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Product attribute filters in 'key:value' format. Repeat for
            multiple values. Same key = OR, different keys = AND.
        variants_attrs (list[str] | Unset): Variant attribute filters in 'key:value' format.
            Returns products that have at least one variant matching all filters. Same key = OR,
            different keys = AND.
        price (None | str | Unset): Whitespace-separated variant price search tokens (shlex-quoted
            for values containing spaces). Returns products with at least one matching variant.
            '<key>>=<value>' / '<key><=<value>' filter the top-level price map. 'loc:<id>',
            'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-only checks any key
            is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'
        variants_availability (None | str | Unset): Variant stock availability filter. Returns
            products that have at least one variant matching, on the same variant as 'variants_attrs'
            and 'price'. A variant is in stock at a location unless its 'locations_availability'
            attribute marks that location 'out_of_stock'; only locations where the variant has a price
            are considered. 'in_stock': in stock at any priced location. 'out_of_stock': has a priced
            location and none is in stock. 'loc:<id>' / 'loc:<id>:in_stock' / 'loc:<id>:out_of_stock'
            restrict this to one location. Any other value returns 422.
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
        Response[HTTPValidationError | PaginatedResponsePartialProduct | PaginatedResponsePartialProductWithVariants | PaginatedResponseProduct | PaginatedResponseProductWithVariants]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        variants_attrs=variants_attrs,
        price=price,
        variants_availability=variants_availability,
        fields=fields,
        include=include,
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
    variants_attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
    variants_availability: None | str | Unset = UNSET,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> (
    HTTPValidationError
    | PaginatedResponsePartialProduct
    | PaginatedResponsePartialProductWithVariants
    | PaginatedResponseProduct
    | PaginatedResponseProductWithVariants
    | None
):
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Product attribute filters in 'key:value' format. Repeat for
            multiple values. Same key = OR, different keys = AND.
        variants_attrs (list[str] | Unset): Variant attribute filters in 'key:value' format.
            Returns products that have at least one variant matching all filters. Same key = OR,
            different keys = AND.
        price (None | str | Unset): Whitespace-separated variant price search tokens (shlex-quoted
            for values containing spaces). Returns products with at least one matching variant.
            '<key>>=<value>' / '<key><=<value>' filter the top-level price map. 'loc:<id>',
            'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-only checks any key
            is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'
        variants_availability (None | str | Unset): Variant stock availability filter. Returns
            products that have at least one variant matching, on the same variant as 'variants_attrs'
            and 'price'. A variant is in stock at a location unless its 'locations_availability'
            attribute marks that location 'out_of_stock'; only locations where the variant has a price
            are considered. 'in_stock': in stock at any priced location. 'out_of_stock': has a priced
            location and none is in stock. 'loc:<id>' / 'loc:<id>:in_stock' / 'loc:<id>:out_of_stock'
            restrict this to one location. Any other value returns 422.
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
        HTTPValidationError | PaginatedResponsePartialProduct | PaginatedResponsePartialProductWithVariants | PaginatedResponseProduct | PaginatedResponseProductWithVariants
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        variants_attrs=variants_attrs,
        price=price,
        variants_availability=variants_availability,
        fields=fields,
        include=include,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    after: None | str | Unset = UNSET,
    before: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    attrs: list[str] | Unset = UNSET,
    variants_attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
    variants_availability: None | str | Unset = UNSET,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> Response[
    HTTPValidationError
    | PaginatedResponsePartialProduct
    | PaginatedResponsePartialProductWithVariants
    | PaginatedResponseProduct
    | PaginatedResponseProductWithVariants
]:
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Product attribute filters in 'key:value' format. Repeat for
            multiple values. Same key = OR, different keys = AND.
        variants_attrs (list[str] | Unset): Variant attribute filters in 'key:value' format.
            Returns products that have at least one variant matching all filters. Same key = OR,
            different keys = AND.
        price (None | str | Unset): Whitespace-separated variant price search tokens (shlex-quoted
            for values containing spaces). Returns products with at least one matching variant.
            '<key>>=<value>' / '<key><=<value>' filter the top-level price map. 'loc:<id>',
            'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-only checks any key
            is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'
        variants_availability (None | str | Unset): Variant stock availability filter. Returns
            products that have at least one variant matching, on the same variant as 'variants_attrs'
            and 'price'. A variant is in stock at a location unless its 'locations_availability'
            attribute marks that location 'out_of_stock'; only locations where the variant has a price
            are considered. 'in_stock': in stock at any priced location. 'out_of_stock': has a priced
            location and none is in stock. 'loc:<id>' / 'loc:<id>:in_stock' / 'loc:<id>:out_of_stock'
            restrict this to one location. Any other value returns 422.
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
        Response[HTTPValidationError | PaginatedResponsePartialProduct | PaginatedResponsePartialProductWithVariants | PaginatedResponseProduct | PaginatedResponseProductWithVariants]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        after=after,
        before=before,
        limit=limit,
        attrs=attrs,
        variants_attrs=variants_attrs,
        price=price,
        variants_availability=variants_availability,
        fields=fields,
        include=include,
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
    variants_attrs: list[str] | Unset = UNSET,
    price: None | str | Unset = UNSET,
    variants_availability: None | str | Unset = UNSET,
    fields: None | str | Unset = UNSET,
    include: None | str | Unset = UNSET,
) -> (
    HTTPValidationError
    | PaginatedResponsePartialProduct
    | PaginatedResponsePartialProductWithVariants
    | PaginatedResponseProduct
    | PaginatedResponseProductWithVariants
    | None
):
    """List Products

     Retrieve a list of all products for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        after (None | str | Unset): Cursor for forward pagination
        before (None | str | Unset): Cursor for backward pagination
        limit (int | Unset):  Default: 20.
        attrs (list[str] | Unset): Product attribute filters in 'key:value' format. Repeat for
            multiple values. Same key = OR, different keys = AND.
        variants_attrs (list[str] | Unset): Variant attribute filters in 'key:value' format.
            Returns products that have at least one variant matching all filters. Same key = OR,
            different keys = AND.
        price (None | str | Unset): Whitespace-separated variant price search tokens (shlex-quoted
            for values containing spaces). Returns products with at least one matching variant.
            '<key>>=<value>' / '<key><=<value>' filter the top-level price map. 'loc:<id>',
            'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price (id-only checks any key
            is set; id+key checks that key is set; +op adds a range).
            'region:<code>[:<key>[<op><value>]]' does the same for region_price. Example: 'USD>=10
            USD<=50 loc:LOC1:retail>=5 region:US:retail'
        variants_availability (None | str | Unset): Variant stock availability filter. Returns
            products that have at least one variant matching, on the same variant as 'variants_attrs'
            and 'price'. A variant is in stock at a location unless its 'locations_availability'
            attribute marks that location 'out_of_stock'; only locations where the variant has a price
            are considered. 'in_stock': in stock at any priced location. 'out_of_stock': has a priced
            location and none is in stock. 'loc:<id>' / 'loc:<id>:in_stock' / 'loc:<id>:out_of_stock'
            restrict this to one location. Any other value returns 422.
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
        HTTPValidationError | PaginatedResponsePartialProduct | PaginatedResponsePartialProductWithVariants | PaginatedResponseProduct | PaginatedResponseProductWithVariants
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            after=after,
            before=before,
            limit=limit,
            attrs=attrs,
            variants_attrs=variants_attrs,
            price=price,
            variants_availability=variants_availability,
            fields=fields,
            include=include,
        )
    ).parsed
