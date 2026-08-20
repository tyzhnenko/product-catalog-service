import shlex
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter, build_price_search_filter
from src.domain.products import ProductsService
from src.domain.types.products import NewProduct, Product, ProductRef, UpdateProduct
from src.domain.types.stores import StoreRef
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
    store_id: StoreRef,
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
    price: str | None = Query(
        None,
        description=(
            "Whitespace-separated variant price search tokens (shlex-quoted for values containing spaces). "
            "Returns products with at least one matching variant. "
            "'<key>>=<value>' / '<key><=<value>' filter the top-level price map. "
            "'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price "
            "(id-only checks any key is set; id+key checks that key is set; +op adds a range). "
            "'region:<code>[:<key>[<op><value>]]' does the same for region_price. "
            "Example: 'USD>=10 USD<=50 loc:LOC1:retail>=5 region:US:retail'"
        ),
    ),
) -> PaginatedResponse[Product]:
    """List all products for a specific store."""
    filters = build_attribute_filter(attrs)
    variant_filters = {
        **build_attribute_filter(variants_attrs),
        **build_price_search_filter(shlex.split(price) if price else []),
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
    store_id: StoreRef,
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
    store_id: StoreRef,
    product_id: ProductRef,
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
    store_id: StoreRef,
    product_id: ProductRef,
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
    store_id: StoreRef,
    product_id: ProductRef,
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
