from uuid import uuid7

import pendulum

from src.domain.types.categories import Category, CategoryUUID, NewCategory, UpdateCategory
from src.domain.types.stores import StoreUUID
from src.models.categories import CategoryModel
from src.models.stores import StoreModel


class CategoriesService:
    async def create_category(self, store_id: StoreUUID, new_category: NewCategory) -> Category | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        category = CategoryModel(
            id=uuid7(),
            store_id=store_id,
            name=new_category.name,
            description=new_category.description,
            status=new_category.status,
            path=new_category.path,
            paths=new_category.paths,
            seo=new_category.seo,
            attributes=new_category.attributes or {},
            images=new_category.images,
        )
        category = await category.create()

        return Category.model_validate(category.model_dump())

    async def list_categories(self, store_id: StoreUUID) -> list[Category] | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        categories = await CategoryModel.find({"store_id": store_id, "deleted_at": None}).to_list()
        return [Category.model_validate(category.model_dump()) for category in categories]

    async def get_category(self, store_id: StoreUUID, category_id: CategoryUUID) -> Category | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        category = await CategoryModel.get(category_id)
        if category and category.store_id == store_id and category.deleted_at is None:
            return Category.model_validate(category.model_dump())
        return None

    async def update_category(
        self,
        store_id: StoreUUID,
        category_id: CategoryUUID,
        update_data: UpdateCategory,
    ) -> Category | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return None

        category = await CategoryModel.get(category_id)
        if not category or category.store_id != store_id or category.deleted_at is not None:
            return None

        # Update only fields that were explicitly set
        update_dict = update_data.model_dump(exclude_unset=True)

        # Handle path update specially to regenerate paths
        if "path" in update_dict:
            category.path = update_dict["path"]
            category.paths = CategoryModel.parse_path(update_dict["path"])
            update_dict.pop("path")  # Remove so it's not set again in the loop

        for field, value in update_dict.items():
            setattr(category, field, value)

        await category.save()
        return Category.model_validate(category.model_dump())

    async def delete_category(self, store_id: StoreUUID, category_id: CategoryUUID) -> bool:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            return False

        category = await CategoryModel.get(category_id)
        if not category or category.store_id != store_id or category.deleted_at is not None:
            return False

        category.deleted_at = pendulum.now()
        await category.save()
        return True
