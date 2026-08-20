from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.new_product import NewProduct
from ...models.product import Product
from ...types import Response


def _get_kwargs(
    store_id: str,
    *,
    body: NewProduct,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/products/{store_id}".format(
            store_id=quote(str(store_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | Product | None:
    if response.status_code == 200:
        response_200 = Product.from_dict(response.json())

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
) -> Response[HTTPValidationError | Product]:
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
    body: NewProduct,
) -> Response[HTTPValidationError | Product]:
    """Create Product

     Create a new product for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        body (NewProduct): Data required to create a new product

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Product]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
    body: NewProduct,
) -> HTTPValidationError | Product | None:
    """Create Product

     Create a new product for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        body (NewProduct): Data required to create a new product

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Product
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    body: NewProduct,
) -> Response[HTTPValidationError | Product]:
    """Create Product

     Create a new product for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        body (NewProduct): Data required to create a new product

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | Product]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
    body: NewProduct,
) -> HTTPValidationError | Product | None:
    """Create Product

     Create a new product for a specific store.

    Args:
        store_id (str): Store ID or slug ref (prefixed 's-')
        body (NewProduct): Data required to create a new product

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | Product
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            body=body,
        )
    ).parsed
