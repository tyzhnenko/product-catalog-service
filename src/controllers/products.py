from decimal import Decimal
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.types import PaginatedResponse
from src.core.utils import (
    build_attribute_filter,
    build_location_price_filter,
    build_price_filter,
    build_region_price_filter,
)
from src.domain.products import ProductsService
from src.domain.types.products import NewProduct, Product, ProductID, UpdateProduct
from src.domain.types.stores import StoreID
from src.settings import load_settings

_settings = load_settings()
router = APIRouter()


@router.get(
    "/{store_id}",
    name="List Products",
    description="Retrieve a list of all products for a specific store.",
    operation_id="list_products",
    dependencies=[Security(ro_access)],
)
async def list_products(
    store_id: StoreID,
    service: Annotated[ProductsService, Depends(ProductsService)],
    after: str | None = Query(None, description="Cursor for forward pagination"),
    before: str | None = Query(None, description="Cursor for backward pagination"),
    limit: int = Query(_settings.pagination.default_limit, ge=1, le=_settings.pagination.max_limit),
    attrs: list[str] = Query(
        default=[],
        description=(
            "Product attribute filters in 'key:value' format. Repeat for multiple values. "
            "Same key = OR, different keys = AND."
        ),
    ),
    variants_attrs: list[str] = Query(
        default=[],
        description=(
            "Variant attribute filters in 'key:value' format. Returns products that have at least one "
            "variant matching all filters. Same key = OR, different keys = AND."
        ),
    ),
    price_key: str | None = Query(None, description="Variant price map key to filter on (e.g. 'USD')"),
    price_min: Decimal | None = Query(None, description="Minimum variant price value (inclusive)"),
    price_max: Decimal | None = Query(None, description="Maximum variant price value (inclusive)"),
    location_price_id: str | None = Query(
        None, description="Location ID - returns products with a variant priced at this location"
    ),
    location_price_key: str | None = Query(None, description="Price key within the location price map"),
    location_price_min: Decimal | None = Query(None, description="Minimum location price value (inclusive)"),
    location_price_max: Decimal | None = Query(None, description="Maximum location price value (inclusive)"),
    region_price_code: str | None = Query(
        None, description="Region/country code for region price filtering (ISO 3166-1 alpha-2)"
    ),
    region_price_key: str | None = Query(None, description="Price key within the region price map"),
    region_price_min: Decimal | None = Query(None, description="Minimum region price value (inclusive)"),
    region_price_max: Decimal | None = Query(None, description="Maximum region price value (inclusive)"),
) -> PaginatedResponse[Product]:
    """List all products for a specific store."""
    filters = build_attribute_filter(attrs)
    variant_filters = {
        **build_attribute_filter(variants_attrs),
        **build_price_filter(price_key, price_min, price_max),
        **build_location_price_filter(location_price_id, location_price_key, location_price_min, location_price_max),
        **build_region_price_filter(region_price_code, region_price_key, region_price_min, region_price_max),
    }
    result = await service.list_products(
        store_id,
        after=after,
        before=before,
        limit=limit,
        filters=filters or None,
        variant_filters=variant_filters or None,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return result


@router.post(
    "/{store_id}",
    name="Create Product",
    description="Create a new product for a specific store.",
    operation_id="create_product",
    dependencies=[Security(rw_access)],
)
async def create_product(
    store_id: StoreID,
    new_product: NewProduct,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Product:
    """Create a new product for a specific store."""
    product = await service.create_product(store_id, new_product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return product


@router.get(
    "/{store_id}/{product_id}",
    name="Get Product",
    description="Retrieve a specific product by its unique identifier.",
    operation_id="get_product",
    dependencies=[Security(ro_access)],
)
async def get_product(
    store_id: StoreID,
    product_id: ProductID,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Product:
    """Get a specific product by ID."""
    product = await service.get_product(store_id, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.patch(
    "/{store_id}/{product_id}",
    name="Update Product",
    description="Update a specific product's information.",
    operation_id="update_product",
    dependencies=[Security(rw_access)],
)
async def update_product(
    store_id: StoreID,
    product_id: ProductID,
    update_data: UpdateProduct,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Product:
    """Update a product's information."""
    updated_product = await service.update_product(store_id, product_id, update_data)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return updated_product


@router.delete(
    "/{store_id}/{product_id}",
    name="Delete Product",
    description="Delete a specific product (soft delete).",
    operation_id="delete_product",
    dependencies=[Security(rw_access)],
)
async def delete_product(
    store_id: StoreID,
    product_id: ProductID,
    service: Annotated[ProductsService, Depends(ProductsService)],
) -> Response:
    """Delete a product (soft delete)."""
    success = await service.delete_product(store_id, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
