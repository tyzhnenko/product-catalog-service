from uuid import uuid7

import pendulum

from src.domain.types.stores import NewStore, Store, StoreUUID, UpdateStore
from src.models.stores import StoreModel


class StoresService:
    async def create_store(self, new_store: NewStore) -> Store:
        store = StoreModel(
            id=uuid7(),
            name=new_store.name,
            url=new_store.url,
        )
        store = await store.create()

        return Store.model_validate(store)

    async def list_stores(self) -> list[Store]:
        stores = await StoreModel.find_all().to_list()
        return [Store.model_validate(store) for store in stores]

    async def get_store(self, store_id: StoreUUID) -> Store | None:
        store = await StoreModel.get(store_id)
        if store:
            return Store.model_validate(store)
        return None

    async def update_store(
        self,
        store_id: StoreUUID,
        update_data: UpdateStore,
    ) -> Store | None:
        store = await StoreModel.get(store_id)
        if not store:
            return None

        if update_data.name is not None:
            store.name = update_data.name
        if update_data.url is not None:
            store.url = update_data.url

        await store.save()
        return Store.model_validate(store)

    async def delete_store(self, store_id: StoreUUID) -> bool:
        store = await StoreModel.get(store_id)
        if not store:
            return False

        store.deleted_at = pendulum.now()
        await store.save()
        return True
