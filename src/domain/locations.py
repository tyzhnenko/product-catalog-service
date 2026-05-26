# from uuid import uuid7

import pendulum

from src.core.types import PaginatedResponse
from src.core.utils import paginate
from src.domain.types.locations import Location, LocationID, NewLocation, UpdateLocation
from src.domain.types.stores import StoreID
from src.models.locations import LocationModel
from src.models.stores import StoreModel


class LocationsService:
    async def create_location(self, store_id: StoreID, new_location: NewLocation) -> Location | None:
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return None

        location = LocationModel(
            # id=uuid7(),
            name=new_location.name,
            store_id=store_id,
            attributes=new_location.attributes,
        )
        location = await location.create()

        return Location.model_validate(location)

    async def list_locations(
        self,
        store_id: StoreID,
        after: str | None,
        before: str | None,
        limit: int,
    ) -> PaginatedResponse[Location] | None:
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return None

        return await paginate(
            LocationModel.find({"store_id": store_id, "deleted_at": None}),
            after,
            before,
            limit,
            transform=Location.model_validate,
        )

    async def get_location(self, store_id: StoreID, location_id: LocationID) -> Location | None:
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return None

        location = await LocationModel.find(
            {"_id": location_id, "store_id": store_id, "deleted_at": None}
        ).first_or_none()
        if location:
            return Location.model_validate(location)
        return None

    async def update_location(
        self,
        store_id: StoreID,
        location_id: LocationID,
        update_data: UpdateLocation,
    ) -> Location | None:
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return None

        location = await LocationModel.find(
            {"_id": location_id, "store_id": store_id, "deleted_at": None}
        ).first_or_none()
        if not location:
            return None

        if update_data.name is not None:
            location.name = update_data.name

        if update_data.attributes is not None:
            location.attributes = update_data.attributes

        await location.save()
        return Location.model_validate(location)

    async def delete_location(self, store_id: StoreID, location_id: LocationID) -> bool:
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return False

        location = await LocationModel.find(
            {"_id": location_id, "store_id": store_id, "deleted_at": None}
        ).first_or_none()
        if not location:
            return False

        location.deleted_at = pendulum.now()
        await location.save()
        return True
