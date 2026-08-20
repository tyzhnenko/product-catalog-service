# from uuid import uuid7

import pendulum
from pymongo.errors import DuplicateKeyError

from src.core.types import PaginatedResponse
from src.core.utils import paginate, parse_ref, raise_for_duplicate_key
from src.domain.types.categories import Category, NewCategory, UpdateCategory
from src.models.categories import CategoryModel
from src.models.stores import StoreModel


class CategoriesService:
    async def create_category(self, store_id: str, new_category: NewCategory) -> Category | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store or store.id is None:
            return None

        category = CategoryModel(
            # id=uuid7(),
            store_id=store.id,
            name=new_category.name,
            description=new_category.description,
            status=new_category.status,
            path=new_category.path,
            paths=new_category.paths,
            seo=new_category.seo,
            attributes=new_category.attributes or {},
            images=new_category.images,
        )
        try:
            category = await category.create()
        except DuplicateKeyError as exc:
            raise_for_duplicate_key(exc)

        return Category.model_validate(category.model_dump())

    async def list_categories(
        self,
        store_id: str,
        after: str | None,
        before: str | None,
        limit: int,
        filters: dict | None = None,
    ) -> PaginatedResponse[Category] | None:
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return None

        query_filter = {"store_id": store.id, "deleted_at": None, **(filters or {})}
        return await paginate(
            CategoryModel.find(query_filter),
            after,
            before,
            limit,
            transform=Category.model_validate,
        )

    async def get_category(self, store_id: str, category_id: str) -> Category | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return None

        category = await CategoryModel.find(
            {**parse_ref(category_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if category:
            return Category.model_validate(category.model_dump())
        return None

    async def update_category(
        self,
        store_id: str,
        category_id: str,
        update_data: UpdateCategory,
    ) -> Category | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return None

        category = await CategoryModel.find(
            {**parse_ref(category_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if not category:
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

        try:
            await category.save()
        except DuplicateKeyError as exc:
            raise_for_duplicate_key(exc)
        return Category.model_validate(category.model_dump())

    async def delete_category(self, store_id: str, category_id: str) -> bool:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            return False

        category = await CategoryModel.find(
            {**parse_ref(category_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if not category:
            return False

        category.deleted_at = pendulum.now()
        await category.save()
        return True
