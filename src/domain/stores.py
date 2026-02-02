# from uuid import uuid7

import pendulum

from src.core.logging import logger
from src.domain.types.stores import NewStore, Store, StoreID, UpdateStore
from src.models.bundles import BundleModel
from src.models.categories import CategoryModel
from src.models.locations import LocationModel
from src.models.products import ProductModel
from src.models.stores import StoreModel
from src.models.variants import VariantModel


class StoresService:
    async def create_store(self, new_store: NewStore) -> Store:
        store = StoreModel(
            name=new_store.name,
            url=new_store.url,
        )
        store = await store.create()

        return Store.model_validate(store)

    async def list_stores(self) -> list[Store]:
        stores = await StoreModel.find({"deleted_at": None}).to_list()
        return [Store.model_validate(store) for store in stores]

    async def get_store(self, store_id: StoreID) -> Store | None:
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if store:
            return Store.model_validate(store)
        return None

    async def update_store(
        self,
        store_id: StoreID,
        update_data: UpdateStore,
    ) -> Store | None:
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return None

        if update_data.name is not None:
            store.name = update_data.name
        if update_data.url is not None:
            store.url = update_data.url

        await store.save()
        return Store.model_validate(store)

    async def delete_store(self, store_id: StoreID) -> bool:
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            return False

        now = pendulum.now()

        # Soft delete all nested resources
        # Delete bundles
        bundles_result = await BundleModel.find({"store_id": store_id, "deleted_at": None}).update_many(
            {"$set": {"deleted_at": now}}
        )
        logger.info(f"Soft deleted {getattr(bundles_result, 'modified_count', 0)} bundles for store {store_id}")

        # Delete variants (must be before products)
        variants_result = await VariantModel.find({"store_id": store_id, "deleted_at": None}).update_many(
            {"$set": {"deleted_at": now}}
        )
        logger.info(f"Soft deleted {getattr(variants_result, 'modified_count', 0)} variants for store {store_id}")

        # Delete products
        products_result = await ProductModel.find({"store_id": store_id, "deleted_at": None}).update_many(
            {"$set": {"deleted_at": now}}
        )
        logger.info(f"Soft deleted {getattr(products_result, 'modified_count', 0)} products for store {store_id}")

        # Delete categories
        categories_result = await CategoryModel.find({"store_id": store_id, "deleted_at": None}).update_many(
            {"$set": {"deleted_at": now}}
        )
        logger.info(f"Soft deleted {getattr(categories_result, 'modified_count', 0)} categories for store {store_id}")

        # Delete locations
        locations_result = await LocationModel.find({"store_id": store_id, "deleted_at": None}).update_many(
            {"$set": {"deleted_at": now}}
        )
        logger.info(f"Soft deleted {getattr(locations_result, 'modified_count', 0)} locations for store {store_id}")

        # Finally, delete the store itself
        store.deleted_at = now
        await store.save()
        logger.info(f"Soft deleted store {store_id}")

        return True
