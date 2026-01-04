from typing import Annotated

from fastapi import Depends, HTTPException, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.domain.bundles import BundlesService
from src.domain.types.bundles import Bundle, BundleUUID, NewBundle, UpdateBundle
from src.domain.types.stores import StoreUUID

router = APIRouter()


@router.get("/{store_id}", dependencies=[Security(ro_access)])
async def list_bundles(
    store_id: StoreUUID,
    service: Annotated[BundlesService, Depends(BundlesService)],
) -> list[Bundle]:
    """List all bundles for a specific store."""
    bundles = await service.list_bundles(store_id)
    if bundles is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return bundles


@router.post("/{store_id}", dependencies=[Security(rw_access)])
async def create_bundle(
    store_id: StoreUUID,
    new_bundle: NewBundle,
    service: Annotated[BundlesService, Depends(BundlesService)],
) -> Bundle:
    """Create a new bundle for a specific store."""
    bundle = await service.create_bundle(store_id, new_bundle)
    if not bundle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return bundle


@router.get("/{store_id}/{bundle_id}", dependencies=[Security(ro_access)])
async def get_bundle(
    store_id: StoreUUID,
    bundle_id: BundleUUID,
    service: Annotated[BundlesService, Depends(BundlesService)],
) -> Bundle:
    """Get a specific bundle by ID."""
    bundle = await service.get_bundle(store_id, bundle_id)
    if not bundle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bundle not found",
        )
    return bundle


@router.patch("/{store_id}/{bundle_id}", dependencies=[Security(rw_access)])
async def update_bundle(
    store_id: StoreUUID,
    bundle_id: BundleUUID,
    update_data: UpdateBundle,
    service: Annotated[BundlesService, Depends(BundlesService)],
) -> Bundle:
    """Update a bundle's information."""
    updated_bundle = await service.update_bundle(store_id, bundle_id, update_data)
    if not updated_bundle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bundle not found",
        )
    return updated_bundle


@router.delete("/{store_id}/{bundle_id}", dependencies=[Security(rw_access)])
async def delete_bundle(
    store_id: StoreUUID,
    bundle_id: BundleUUID,
    service: Annotated[BundlesService, Depends(BundlesService)],
) -> Response:
    """Delete a bundle (soft delete)."""
    success = await service.delete_bundle(store_id, bundle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bundle not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
