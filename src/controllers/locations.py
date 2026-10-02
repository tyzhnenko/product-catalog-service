from typing import Annotated

from fastapi import Depends, HTTPException, Query, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.fields import FieldsParams, sparse_response
from src.core.pagination import PaginationParams, pagination_with_sort
from src.core.types import PaginatedResponse
from src.core.utils import build_attribute_filter
from src.domain.locations import LocationsService
from src.domain.types.locations import Location, LocationRef, NewLocation, PartialLocation, UpdateLocation
from src.domain.types.stores import StoreRef

router = APIRouter()

SORT_FIELDS = ("name", "created_at", "updated_at")
SORT_KEYS = ("attr",)


def location_filters(
    attrs: Annotated[
        list[str],
        Query(
            default_factory=list,
            description=(
                "Attribute filters in 'key:value' format. Repeat for multiple values. "
                "Same key = OR, different keys = AND. Prefix the value with '>', '>=', '<' or '<=' for a "
                "numeric or ISO 8601 date range, e.g. 'seats:>=20'."
            ),
        ),
    ],
) -> dict | None:
    return build_attribute_filter(attrs) or None


LocationFilters = Annotated[dict | None, Depends(location_filters)]


@router.get(
    "/{store_id}",
    name="List Locations",
    description="Retrieve a list of all locations for a specific store.",
    operation_id="list_locations",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Location, PartialLocation, paginated=True),
    response_model_exclude_unset=True,
)
async def list_locations(
    store_id: StoreRef,
    service: Annotated[LocationsService, Depends(LocationsService)],
    pagination: Annotated[PaginationParams, Depends(pagination_with_sort(SORT_FIELDS, SORT_KEYS))],
    filters: LocationFilters,
    fields: Annotated[FieldsParams, Depends()],
) -> PaginatedResponse[Location] | PaginatedResponse[PartialLocation]:
    result = await service.list_locations(store_id, pagination, filters=filters, fields=fields.resolve(Location))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return result


@router.post(
    "/{store_id}",
    name="Create Location",
    description="Create a new location for a specific store.",
    operation_id="create_location",
    dependencies=[Security(rw_access)],
)
async def create_location(
    store_id: StoreRef,
    new_location: NewLocation,
    service: Annotated[LocationsService, Depends(LocationsService)],
) -> Location:
    location = await service.create_location(store_id, new_location)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return location


@router.get(
    "/{store_id}/{location_id}",
    name="Get Location",
    description="Retrieve details of a specific location by its ID for a specific store.",
    operation_id="get_location",
    dependencies=[Security(ro_access)],
    response_model=sparse_response(Location, PartialLocation),
    response_model_exclude_unset=True,
)
async def get_location(
    store_id: StoreRef,
    location_id: LocationRef,
    service: Annotated[LocationsService, Depends(LocationsService)],
    fields: Annotated[FieldsParams, Depends()],
) -> Location | PartialLocation:
    location = await service.get_location(store_id, location_id, fields=fields.resolve(Location))
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    return location


@router.put(
    "/{store_id}/{location_id}",
    name="Update Location",
    description="Update details of a specific location by its ID for a specific store.",
    operation_id="update_location",
    dependencies=[Security(rw_access)],
)
async def update_location(
    store_id: StoreRef,
    location_id: LocationRef,
    update_data: UpdateLocation,
    service: Annotated[LocationsService, Depends(LocationsService)],
) -> Location:
    updated_location = await service.update_location(store_id, location_id, update_data)
    if not updated_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )

    return updated_location


@router.delete(
    "/{store_id}/{location_id}",
    name="Delete Location",
    description="Delete a specific location by its ID for a specific store.",
    operation_id="delete_location",
    dependencies=[Security(rw_access)],
)
async def delete_location(
    store_id: StoreRef,
    location_id: LocationRef,
    service: Annotated[LocationsService, Depends(LocationsService)],
):
    success = await service.delete_location(store_id, location_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    raise HTTPException(status_code=204)
