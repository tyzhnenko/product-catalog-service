from typing import Annotated

from fastapi import Depends, HTTPException, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.domain.types.products import ProductUUID
from src.domain.types.stores import StoreUUID
from src.domain.types.variants import (
    NewProductVariant,
    ProductVariant,
    UpdateProductVariant,
    VariantUUID,
)
from src.domain.variants import VariantsService

router = APIRouter()


@router.get("/{store_id}/{product_id}", dependencies=[Security(ro_access)])
async def list_variants(
    store_id: StoreUUID,
    product_id: ProductUUID,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> list[ProductVariant]:
    """List all variants for a specific product."""
    variants = await service.list_variants(store_id, product_id)
    if variants is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or store not found",
        )
    return variants


@router.post("/{store_id}/{product_id}", dependencies=[Security(rw_access)])
async def create_variant(
    store_id: StoreUUID,
    product_id: ProductUUID,
    new_variant: NewProductVariant,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> ProductVariant:
    """Create a new variant for a specific product."""
    variant = await service.create_variant(store_id, product_id, new_variant)
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or store not found",
        )
    return variant


@router.get("/{store_id}/{product_id}/{variant_id}", dependencies=[Security(ro_access)])
async def get_variant(
    store_id: StoreUUID,
    product_id: ProductUUID,
    variant_id: VariantUUID,
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


@router.patch("/{store_id}/{product_id}/{variant_id}", dependencies=[Security(rw_access)])
async def update_variant(
    store_id: StoreUUID,
    product_id: ProductUUID,
    variant_id: VariantUUID,
    update_data: UpdateProductVariant,
    service: Annotated[VariantsService, Depends(VariantsService)],
) -> ProductVariant:
    """Update a variant's information."""
    updated_variant = await service.update_variant(store_id, product_id, variant_id, update_data)
    if not updated_variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found",
        )
    return updated_variant


@router.delete("/{store_id}/{product_id}/{variant_id}", dependencies=[Security(rw_access)])
async def delete_variant(
    store_id: StoreUUID,
    product_id: ProductUUID,
    variant_id: VariantUUID,
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
