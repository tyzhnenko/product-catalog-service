from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.product_variant import ProductVariant
from ...types import Response


def _get_kwargs(
    store_id: str,
    product_id: str,
    variant_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/variants/{store_id}/{product_id}/{variant_id}".format(
            store_id=quote(str(store_id), safe=""),
            product_id=quote(str(product_id), safe=""),
            variant_id=quote(str(variant_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProductVariant | None:
    if response.status_code == 200:
        response_200 = ProductVariant.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProductVariant]:
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
) -> Response[HTTPValidationError | ProductVariant]:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        variant_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProductVariant]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        variant_id=variant_id,
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
) -> HTTPValidationError | ProductVariant | None:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        variant_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProductVariant
    """

    return sync_detailed(
        store_id=store_id,
        product_id=product_id,
        variant_id=variant_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ProductVariant]:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        variant_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProductVariant]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        product_id=product_id,
        variant_id=variant_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    product_id: str,
    variant_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ProductVariant | None:
    """Get Variant

     Retrieve a specific variant by its unique identifier.

    Args:
        store_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        product_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        variant_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProductVariant
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            product_id=product_id,
            variant_id=variant_id,
            client=client,
        )
    ).parsed
