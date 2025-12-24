from uuid import uuid7

import pendulum

from src.domain.types.locations import Location, LocationUUID, NewLocation, UpdateLocation
from src.domain.types.stores import StoreUUID
from src.models.locations import LocationModel
from src.models.stores import StoreModel


class LocationsService:
    async def create_location(self, store_id: StoreUUID, new_location: NewLocation) -> Location | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        location = LocationModel(
            id=uuid7(),
            name=new_location.name,
            store_id=store_id,
        )
        location = await location.create()

        return Location.model_validate(location)

    async def list_locations(self, store_id: StoreUUID) -> list[Location] | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        locations = await LocationModel.find({"store_id": store_id}).to_list()
        return [Location.model_validate(location) for location in locations]

    async def get_location(self, store_id: StoreUUID, location_id: LocationUUID) -> Location | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        location = await LocationModel.get(location_id)
        if location and location.store_id == store_id:
            return Location.model_validate(location)
        return None

    async def update_location(
        self,
        store_id: StoreUUID,
        location_id: LocationUUID,
        update_data: UpdateLocation,
    ) -> Location | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        location = await LocationModel.get(location_id)
        if not location or location.store_id != store_id:
            return None

        if update_data.name is not None:
            location.name = update_data.name

        await location.save()
        return Location.model_validate(location)

    async def delete_location(self, store_id: StoreUUID, location_id: LocationUUID) -> bool:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return False

        location = await LocationModel.get(location_id)
        if not location or location.store_id != store_id:
            return False

        location.deleted_at = pendulum.now()
        await location.save()
        return True
