# from uuid import uuid7

from typing import overload

import pendulum
from pymongo.errors import DuplicateKeyError

from src.core.fields import FieldSelection, projection_model, to_partial
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.core.utils import paginate, parse_ref, raise_for_duplicate_key
from src.domain.types.locations import Location, NewLocation, PartialLocation, UpdateLocation
from src.models.locations import LocationModel
from src.models.stores import StoreModel


class LocationsService:
    async def create_location(self, store_id: str, new_location: NewLocation) -> Location | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store or store.id is None:
            return None

        location = LocationModel(
            # id=uuid7(),
            name=new_location.name,
            store_id=store.id,
            attributes=new_location.attributes,
            seo=new_location.seo,
        )
        try:
            location = await location.create()
        except DuplicateKeyError as exc:
            raise_for_duplicate_key(exc)

        return Location.model_validate(location)

    @overload
    async def list_locations(
        self, store_id: str, pagination: PaginationParams, fields: None = None
    ) -> PaginatedResponse[Location] | None: ...

    @overload
    async def list_locations(
        self, store_id: str, pagination: PaginationParams, fields: FieldSelection = ...
    ) -> PaginatedResponse[PartialLocation] | None: ...

    async def list_locations(
        self,
        store_id: str,
        pagination: PaginationParams,
        fields: FieldSelection | None = None,
    ) -> PaginatedResponse[Location] | PaginatedResponse[PartialLocation] | None:
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return None

        query_filter = {"store_id": store.id, "deleted_at": None}
        if fields:
            return await paginate(
                LocationModel.find(query_filter).project(projection_model(Location, fields.fetch_names(Location))),
                pagination.after,
                pagination.before,
                pagination.limit,
                transform=lambda doc: to_partial(PartialLocation, doc, fields),
            )

        return await paginate(
            LocationModel.find(query_filter),
            pagination.after,
            pagination.before,
            pagination.limit,
            transform=Location.model_validate,
        )

    @overload
    async def get_location(self, store_id: str, location_id: str, fields: None = None) -> Location | None: ...

    @overload
    async def get_location(
        self, store_id: str, location_id: str, fields: FieldSelection = ...
    ) -> PartialLocation | None: ...

    async def get_location(
        self, store_id: str, location_id: str, fields: FieldSelection | None = None
    ) -> Location | PartialLocation | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return None

        query = LocationModel.find({**parse_ref(location_id), "store_id": store.id, "deleted_at": None})
        if fields:
            location = await query.project(projection_model(Location, fields.fetch_names(Location))).first_or_none()
            return to_partial(PartialLocation, location, fields) if location else None

        location = await query.first_or_none()
        if location:
            return Location.model_validate(location)
        return None

    async def update_location(
        self,
        store_id: str,
        location_id: str,
        update_data: UpdateLocation,
    ) -> Location | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return None

        location = await LocationModel.find(
            {**parse_ref(location_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if not location:
            return None

        if update_data.name is not None:
            location.name = update_data.name

        if update_data.attributes is not None:
            location.attributes = update_data.attributes

        if update_data.seo is not None:
            location.seo = update_data.seo

        try:
            await location.save()
        except DuplicateKeyError as exc:
            raise_for_duplicate_key(exc)
        return Location.model_validate(location)

    async def delete_location(self, store_id: str, location_id: str) -> bool:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return False

        location = await LocationModel.find(
            {**parse_ref(location_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if not location:
            return False

        location.deleted_at = pendulum.now()
        await location.save()
        return True
