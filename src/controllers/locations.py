from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from src.domain.locations import LocationsService
from src.domain.types.locations import Location, LocationUUID, NewLocation, UpdateLocation
from src.domain.types.stores import StoreUUID

router = APIRouter()


@router.get("/{store_id}")
async def list_locations(
    store_id: StoreUUID,
    service: Annotated[LocationsService, Depends(LocationsService)],
) -> list[Location]:
    locations = await service.list_locations(store_id)
    if locations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
    return locations


@router.post("/{store_id}")
async def create_location(
    store_id: StoreUUID,
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


@router.get("/{store_id}/{location_id}")
async def get_location(
    store_id: StoreUUID,
    location_id: LocationUUID,
    service: Annotated[LocationsService, Depends(LocationsService)],
) -> Location:
    location = await service.get_location(store_id, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    return location


@router.put("/{store_id}/{location_id}")
async def update_location(
    store_id: StoreUUID,
    location_id: LocationUUID,
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


@router.delete("/{store_id}/{location_id}")
async def delete_location(
    store_id: StoreUUID,
    location_id: LocationUUID,
    service: Annotated[LocationsService, Depends(LocationsService)],
):
    success = await service.delete_location(store_id, location_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    raise HTTPException(status_code=204)
