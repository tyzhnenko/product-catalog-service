import shlex
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.fields import FieldsParams, sparse_response
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter, build_availability_filter, build_price_search_filter
from src.domain.types.products import ProductRef
from src.domain.types.stores import StoreRef
from src.domain.types.variants import (
    NewProductVariant,
    PartialProductVariant,
    ProductVariant,
    UpdateProductVariant,
    VariantRef,
)
from src.domain.variants import DuplicateVariantOptionsError, VariantsService

router = APIRouter()


def variant_filters(
    attrs: Annotated[
        list[str],
        Query(
            default_factory=list,
            description=(
                "Attribute filters in 'key:value' format. Repeat for multiple values. "
                "Same key = OR, different keys = AND."
            ),
        ),
    ],
    price: Annotated[
        str | None,
        Query(
            description=(
                "Whitespace-separated price search tokens (shlex-quoted for values containing spaces). "
                "'<key>>=<value>' / '<key><=<value>' filter the top-level price map. "
                "'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price "
                "(id-only checks any key is set; id+key checks that key is set; +op adds a range). "
                "'region:<code>[:<key>[<op><value>]]' does the same for region_price. "
                "Example: 'USD>=10 USD<=50 loc:LOC1:retail>=5 region:US:retail'"
            ),
        ),
    ] = None,
    availability: Annotated[
        str | None,
        Query(
            description=(
                "Filter by stock availability. A variant is in stock at a location unless its "
                "'locations_availability' attribute marks that location 'out_of_stock'; only locations where the "
                "variant has a price are considered. 'in_stock': in stock at any priced location. "
                "'out_of_stock': has a priced location and none is in stock. "
                "'loc:<id>' / 'loc:<id>:in_stock' / 'loc:<id>:out_of_stock' restrict this to one location. "
                "Combined with 'attrs' and 'price' using AND. Any other value returns 422."
            ),
        ),
    ] = None,
) -> dict | None:
    filters = {
        **build_attribute_filter(attrs),
        **build_price_search_filter(shlex.split(price) if price else []),
        **build_availability_filter(availability),
    }
    return filters or None


VariantFilters = Annotated[dict | None, Depends(variant_filters)]


@router.get(
    "/{store_id}/{product_id}",
    name="List Variants",
    description="Retrieve a list of all variants for a specific product.",
    operation_id="list_variants",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(ProductVariant, PartialProductVariant, paginated=True),
    response_model_exclude_unset=True,
)
async def list_variants(
    store_id: StoreRef,
    product_id: ProductRef,
    service: Annotated[VariantsService, Depends(VariantsService)],
    pagination: Annotated[PaginationParams, Depends()],
    filters: VariantFilters,
    fields: Annotated[FieldsParams, Depends()],
) -> PaginatedResponse[ProductVariant] | PaginatedResponse[PartialProductVariant]:
    """List all variants for a specific product."""
    result = await service.list_variants(
        store_id,
        product_id,
        pagination,
        filters=filters,
        fields=fields.resolve(ProductVariant),
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or store not found",
        )
    return result


@router.post(
    "/{store_id}/{product_id}",
    name="Create Variant",
    description="Create a new variant for a specific product.",
    operation_id="create_variant",
    dependencies=[Security(rw_access)],
)
async def create_variant(
    store_id: StoreRef,
    product_id: ProductRef,
    new_variant: NewProductVariant,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> ProductVariant:
    """Create a new variant for a specific product."""
    try:
        variant = await service.create_variant(store_id, product_id, new_variant)
    except DuplicateVariantOptionsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or store not found",
        )
    return variant


@router.get(
    "/{store_id}/{product_id}/{variant_id}",
    name="Get Variant",
    description="Retrieve a specific variant by its unique identifier.",
    operation_id="get_variant",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(ProductVariant, PartialProductVariant),
    response_model_exclude_unset=True,
)
async def get_variant(
    store_id: StoreRef,
    product_id: ProductRef,
    variant_id: VariantRef,
    service: Annotated[VariantsService, Depends(VariantsService)],
    fields: Annotated[FieldsParams, Depends()],
) -> ProductVariant | PartialProductVariant:
    """Get a specific variant by ID."""
    variant = await service.get_variant(store_id, product_id, variant_id, fields=fields.resolve(ProductVariant))
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found",
        )
    return variant


@router.patch(
    "/{store_id}/{product_id}/{variant_id}",
    name="Update Variant",
    description="Update a specific variant's information.",
    operation_id="update_variant",
    dependencies=[Security(rw_access)],
)
async def update_variant(
    store_id: StoreRef,
    product_id: ProductRef,
    variant_id: VariantRef,
    update_data: UpdateProductVariant,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> ProductVariant:
    """Update a variant's information."""
    try:
        updated_variant = await service.update_variant(store_id, product_id, variant_id, update_data)
    except DuplicateVariantOptionsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    if not updated_variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found",
        )
    return updated_variant


@router.delete(
    "/{store_id}/{product_id}/{variant_id}",
    name="Delete Variant",
    description="Delete a specific variant (soft delete).",
    operation_id="delete_variant",
    dependencies=[Security(rw_access)],
)
async def delete_variant(
    store_id: StoreRef,
    product_id: ProductRef,
    variant_id: VariantRef,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> Response:
    """Delete a variant (soft delete)."""
    success = await service.delete_variant(store_id, product_id, variant_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
