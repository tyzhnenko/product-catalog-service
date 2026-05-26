from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.types import PaginatedResponse
from src.domain.types.products import ProductID
from src.domain.types.stores import StoreID
from src.domain.types.variants import (
    NewProductVariant,
    ProductVariant,
    UpdateProductVariant,
    VariantID,
)
from src.domain.variants import DuplicateVariantOptionsError, VariantsService
from src.settings import load_settings

_settings = load_settings()
router = APIRouter()


@router.get(
    "/{store_id}/{product_id}",
    name="List Variants",
    description="Retrieve a list of all variants for a specific product.",
    operation_id="list_variants",
    dependencies=[Security(ro_access)],
)
async def list_variants(
    store_id: StoreID,
    product_id: ProductID,
    service: Annotated[VariantsService, Depends(VariantsService)],
    after: str | None = Query(None, description="Cursor for forward pagination"),
    before: str | None = Query(None, description="Cursor for backward pagination"),
    limit: int = Query(_settings.pagination.default_limit, ge=1, le=_settings.pagination.max_limit),
) -> PaginatedResponse[ProductVariant]:
    """List all variants for a specific product."""
    result = await service.list_variants(store_id, product_id, after=after, before=before, limit=limit)
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
    store_id: StoreID,
    product_id: ProductID,
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
)
async def get_variant(
    store_id: StoreID,
    product_id: ProductID,
    variant_id: VariantID,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> ProductVariant:
    """Get a specific variant by ID."""
    variant = await service.get_variant(store_id, product_id, variant_id)
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
    store_id: StoreID,
    product_id: ProductID,
    variant_id: VariantID,
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
    store_id: StoreID,
    product_id: ProductID,
    variant_id: VariantID,
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
