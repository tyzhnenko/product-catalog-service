import shlex
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Response, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.fields import FieldsParams, sparse_response
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter, build_price_search_filter
from src.domain.bundles import BundlesService
from src.domain.types.bundles import Bundle, BundleRef, NewBundle, PartialBundle, UpdateBundle
from src.domain.types.stores import StoreRef

router = APIRouter()


def bundle_filters(
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
) -> dict | None:
    filters = {
        **build_attribute_filter(attrs),
        **build_price_search_filter(shlex.split(price) if price else []),
    }
    return filters or None


BundleFilters = Annotated[dict | None, Depends(bundle_filters)]


@router.get(
    "/{store_id}",
    name="List Bundles",
    description="List all bundles for a specific store.",
    operation_id="list_bundles",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Bundle, PartialBundle, paginated=True),
    response_model_exclude_unset=True,
)
async def list_bundles(
    store_id: StoreRef,
    service: Annotated[BundlesService, Depends(BundlesService)],
    pagination: Annotated[PaginationParams, Depends()],
    filters: BundleFilters,
    fields: Annotated[FieldsParams, Depends()],
) -> PaginatedResponse[Bundle] | PaginatedResponse[PartialBundle]:
    """List all bundles for a specific store."""
    result = await service.list_bundles(
        store_id,
        pagination,
        filters=filters,
        fields=fields.resolve(Bundle),
    )
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
    store_id: StoreRef,
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
    response_model=sparse_response(Bundle, PartialBundle),
    response_model_exclude_unset=True,
)
async def get_bundle(
    store_id: StoreRef,
    bundle_id: BundleRef,
    service: Annotated[BundlesService, Depends(BundlesService)],
    fields: Annotated[FieldsParams, Depends()],
) -> Bundle | PartialBundle:
    """Get a specific bundle by ID."""
    bundle = await service.get_bundle(store_id, bundle_id, fields=fields.resolve(Bundle))
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
    store_id: StoreRef,
    bundle_id: BundleRef,
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
    store_id: StoreRef,
    bundle_id: BundleRef,
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
