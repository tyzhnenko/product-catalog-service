import shlex
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.fields import FieldsParams, sparse_response
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter, build_availability_filter, build_price_search_filter
from src.domain.products import ProductsService
from src.domain.types.products import NewProduct, PartialProduct, Product, ProductRef, UpdateProduct
from src.domain.types.stores import StoreRef
from src.domain.types.variants import PartialProductWithVariants, ProductWithVariants

router = APIRouter()


@dataclass
class ProductFilters:
    filters: dict | None
    variant_filters: dict | None


def product_filters(
    attrs: Annotated[
        list[str],
        Query(
            default_factory=list,
            description=(
                "Product attribute filters in 'key:value' format. Repeat for multiple values. "
                "Same key = OR, different keys = AND."
            ),
        ),
    ],
    variants_attrs: Annotated[
        list[str],
        Query(
            default_factory=list,
            description=(
                "Variant attribute filters in 'key:value' format. Returns products that have at least one "
                "variant matching all filters. Same key = OR, different keys = AND."
            ),
        ),
    ],
    price: Annotated[
        str | None,
        Query(
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
    ] = None,
    variants_availability: Annotated[
        str | None,
        Query(
            description=(
                "Variant stock availability filter. Returns products that have at least one variant matching, "
                "on the same variant as 'variants_attrs' and 'price'. A variant is in stock at a location unless its "
                "'locations_availability' attribute marks that location 'out_of_stock'; only locations where the "
                "variant has a price are considered. 'in_stock': in stock at any priced location. "
                "'out_of_stock': has a priced location and none is in stock. "
                "'loc:<id>' / 'loc:<id>:in_stock' / 'loc:<id>:out_of_stock' restrict this to one location. "
                "Any other value returns 422."
            ),
        ),
    ] = None,
) -> ProductFilters:
    variant_filters = {
        **build_attribute_filter(variants_attrs),
        **build_price_search_filter(shlex.split(price) if price else []),
        **build_availability_filter(variants_availability),
    }
    return ProductFilters(
        filters=build_attribute_filter(attrs) or None,
        variant_filters=variant_filters or None,
    )


SUPPORTED_INCLUDES = frozenset({"variants"})


@dataclass
class IncludeParams:
    include: str | None = Query(
        None,
        description="Comma-separated relations to embed in the response. Supported: `variants`.",
    )

    def resolve(self) -> frozenset[str]:
        """Validate the raw param and return the set of relations to embed; empty when `include` was omitted."""
        if self.include is None:
            return frozenset()
        values = [value.strip() for value in self.include.split(",")]
        if not values or not all(values):
            raise HTTPException(status_code=422, detail="Empty relation name in `include`")
        value_set = frozenset(values)
        if unknown := value_set - SUPPORTED_INCLUDES:
            raise HTTPException(status_code=422, detail=f"Unsupported include value(s): {sorted(unknown)}")
        return value_set


@router.get(
    "/{store_id}",
    name="List Products",
    description="Retrieve a list of all products for a specific store.",
    operation_id="list_products",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(
        ProductWithVariants, PartialProductWithVariants, Product, PartialProduct, paginated=True
    ),
    response_model_exclude_unset=True,
)
async def list_products(
    store_id: StoreRef,
    service: Annotated[ProductsService, Depends(ProductsService)],
    pagination: Annotated[PaginationParams, Depends()],
    filters: Annotated[ProductFilters, Depends(product_filters)],
    fields: Annotated[FieldsParams, Depends()],
    include: Annotated[IncludeParams, Depends()],
) -> (
    PaginatedResponse[ProductWithVariants]
    | PaginatedResponse[PartialProductWithVariants]
    | PaginatedResponse[Product]
    | PaginatedResponse[PartialProduct]
):
    """List all products for a specific store."""
    result = await service.list_products(
        store_id,
        pagination,
        filters=filters.filters,
        variant_filters=filters.variant_filters,
        fields=fields.resolve(Product),
        include_variants="variants" in include.resolve(),
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
    response_model=sparse_response(ProductWithVariants, PartialProductWithVariants, Product, PartialProduct),
    response_model_exclude_unset=True,
)
async def get_product(
    store_id: StoreRef,
    product_id: ProductRef,
    service: Annotated[ProductsService, Depends(ProductsService)],
    fields: Annotated[FieldsParams, Depends()],
    include: Annotated[IncludeParams, Depends()],
) -> ProductWithVariants | PartialProductWithVariants | Product | PartialProduct:
    """Get a specific product by ID."""
    product = await service.get_product(
        store_id, product_id, fields=fields.resolve(Product), include_variants="variants" in include.resolve()
    )
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
