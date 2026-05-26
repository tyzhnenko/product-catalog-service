from typing import Annotated

from fastapi import Depends, HTTPException, Query, Security, status
from fastapi.routing import APIRouter

from src.core.auth import ro_access, rw_access
from src.core.types import PaginatedResponse
from src.domain.locations import LocationsService
from src.domain.types.locations import Location, LocationID, NewLocation, UpdateLocation
from src.domain.types.stores import StoreID
from src.settings import load_settings

_settings = load_settings()
router = APIRouter()


@router.get(
    "/{store_id}",
    name="List Locations",
    description="Retrieve a list of all locations for a specific store.",
    operation_id="list_locations",
    dependencies=[Security(ro_access)],
)
async def list_locations(
    store_id: StoreID,
    service: Annotated[LocationsService, Depends(LocationsService)],
    after: str | None = Query(None, description="Cursor for forward pagination"),
    before: str | None = Query(None, description="Cursor for backward pagination"),
    limit: int = Query(_settings.pagination.default_limit, ge=1, le=_settings.pagination.max_limit),
) -> PaginatedResponse[Location]:
    result = await service.list_locations(store_id, after=after, before=before, limit=limit)
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
    store_id: StoreID,
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
)
async def get_location(
    store_id: StoreID,
    location_id: LocationID,
    service: Annotated[LocationsService, Depends(LocationsService)],
) -> Location:
    location = await service.get_location(store_id, location_id)
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
    store_id: StoreID,
    location_id: LocationID,
    update_data: UpdateLocation,
    service: Annotated[LocationsService, Depends(LocationsService)],
):
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
    store_id: StoreID,
    location_id: LocationID,
    service: Annotated[LocationsService, Depends(LocationsService)],
):
    success = await service.delete_location(store_id, location_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    raise HTTPException(status_code=204)
