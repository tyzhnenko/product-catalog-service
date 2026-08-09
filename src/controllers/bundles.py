import shlex
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter, build_price_search_filter
from src.domain.bundles import BundlesService
from src.domain.types.bundles import Bundle, BundleID, NewBundle, UpdateBundle
from src.domain.types.stores import StoreID
from src.settings import load_settings

_settings = load_settings()
router = APIRouter()


@router.get(
    "/{store_id}",
    name="List Bundles",
    description="List all bundles for a specific store.",
    operation_id="list_bundles",
    dependencies=[Security(ro_access)],
)
async def list_bundles(
    store_id: StoreID,
    service: Annotated[BundlesService, Depends(BundlesService)],
    after: str | None = Query(None, description="Cursor for forward pagination"),
    before: str | None = Query(None, description="Cursor for backward pagination"),
    limit: int = Query(_settings.pagination.default_limit, ge=1, le=_settings.pagination.max_limit),
    attrs: list[str] = Query(
        default_factory=list,
        description=(
            "Attribute filters in 'key:value' format. Repeat for multiple values. Same key = OR, different keys = AND."
        ),
    ),
    price: str | None = Query(
        None,
        description=(
            "Whitespace-separated price search tokens (shlex-quoted for values containing spaces). "
            "'<key>>=<value>' / '<key><=<value>' filter the top-level price map. "
            "'loc:<id>', 'loc:<id>:<key>', 'loc:<id>:<key>>=<value>' filter location_price "
            "(id-only checks any key is set; id+key checks that key is set; +op adds a range). "
            "'region:<code>[:<key>[<op><value>]]' does the same for region_price. "
            "Example: 'USD>=10 USD<=50 loc:LOC1:retail>=5 region:US:retail'"
        ),
    ),
) -> PaginatedResponse[Bundle]:
    """List all bundles for a specific store."""
    filters = {
        **build_attribute_filter(attrs),
        **build_price_search_filter(shlex.split(price) if price else []),
    }
    result = await service.list_bundles(store_id, after=after, before=before, limit=limit, filters=filters or None)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return result


@router.post(
    "/{store_id}",
    name="Create Bundle",
    description="Create a new bundle for a specific store.",
    operation_id="create_bundle",
    dependencies=[Security(rw_access)],
)
async def create_bundle(
    store_id: StoreID,
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


@router.get(
    "/{store_id}/{bundle_id}",
    name="Get Bundle",
    description="Get a specific bundle by ID.",
    operation_id="get_bundle",
    dependencies=[Security(ro_access)],
)
async def get_bundle(
    store_id: StoreID,
    bundle_id: BundleID,
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


@router.patch(
    "/{store_id}/{bundle_id}",
    name="Update Bundle",
    description="Update a bundle's information.",
    operation_id="update_bundle",
    dependencies=[Security(rw_access)],
)
async def update_bundle(
    store_id: StoreID,
    bundle_id: BundleID,
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


@router.delete(
    "/{store_id}/{bundle_id}",
    name="Delete Bundle",
    description="Delete a bundle.",
    operation_id="delete_bundle",
    dependencies=[Security(rw_access)],
)
async def delete_bundle(
    store_id: StoreID,
    bundle_id: BundleID,
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
