# from uuid import uuid7

from typing import cast

import pendulum
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from src.core.logging import logger
from src.core.types import PaginatedResponse
from src.core.utils import paginate, parse_ref, raise_for_duplicate_key
from src.domain.types.categories import CategoryID
from src.domain.types.products import (
    NewProduct,
    Product,
    ProductID,
    ProductStatusEnum,
    UpdateProduct,
)
from src.domain.types.stores import StoreID
from src.models.categories import CategoryModel
from src.models.products import ProductModel
from src.models.stores import StoreModel
from src.models.variants import VariantModel


class _VariantProductIdProjection(BaseModel):
    product_id: ProductID


class ProductsService:
    async def _sanitize_categories(self, store_id: StoreID, category_ids: list[CategoryID]) -> list[CategoryID]:
        """Filter category IDs to only include valid ones that exist and belong to the specified store."""
        if not category_ids:
            return []

        # Get all categories in one query
        categories = await CategoryModel.find(
            {"_id": {"$in": category_ids}, "store_id": store_id, "deleted_at": None}
        ).to_list()

        # Return only valid category IDs
        valid_ids: list[CategoryID] = [cat.id for cat in categories]  # type: ignore[misc]

        # Log if any categories were filtered out
        if len(valid_ids) != len(category_ids):
            found_ids = {str(cat.id) for cat in categories}
            requested_ids = {str(cat_id) for cat_id in category_ids}
            filtered_ids = requested_ids - found_ids
            logger.info(
                f"Filtered out invalid categories for store {store_id}: {filtered_ids}. "
                f"Kept {len(valid_ids)} valid categories."
            )

        return valid_ids

    async def create_product(self, store_id: str, new_product: NewProduct) -> Product | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store or store.id is None:
            logger.warning(f"Store not found: {store_id}")
            return None

        # Sanitize categories - keep only valid ones
        valid_categories = await self._sanitize_categories(cast(StoreID, store.id), new_product.categories or [])

        product = ProductModel(
            # id=uuid7(),
            store_id=store.id,
            name=new_product.name,
            description=new_product.description,
            brand=new_product.brand,
            tags=new_product.tags,
            seo=new_product.seo,
            status=ProductStatusEnum.ACTIVE,
            attributes=new_product.attributes or {},
            categories=valid_categories,
        )
        try:
            product = await product.create()
        except DuplicateKeyError as exc:
            raise_for_duplicate_key(exc)
        logger.info(f"Created product {product.id} for store {store.id}")

        return Product.model_validate(product)

    async def list_products(
        self,
        store_id: str,
        after: str | None,
        before: str | None,
        limit: int,
        filters: dict | None = None,
        variant_filters: dict | None = None,
    ) -> PaginatedResponse[Product] | None:
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        query_filter = {"store_id": store.id, "deleted_at": None, **(filters or {})}

        if variant_filters:
            variant_query = {"store_id": store.id, "deleted_at": None, **variant_filters}
            variants = await VariantModel.find(variant_query).project(_VariantProductIdProjection).to_list()
            product_ids = list({variant.product_id for variant in variants})
            query_filter["_id"] = {"$in": product_ids}

        return await paginate(
            ProductModel.find(query_filter),
            after,
            before,
            limit,
            transform=Product.model_validate,
        )

    async def get_product(self, store_id: str, product_id: str) -> Product | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        product = await ProductModel.find(
            {**parse_ref(product_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if product:
            return Product.model_validate(product)
        logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
        return None

    async def update_product(
        self,
        store_id: str,
        product_id: str,
        update_data: UpdateProduct,
    ) -> Product | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        product = await ProductModel.find(
            {**parse_ref(product_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        # Update only fields that were explicitly set
        update_dict = update_data.model_dump(exclude_unset=True)

        # Sanitize categories if they are being updated
        if "categories" in update_dict and update_dict["categories"] is not None:
            update_dict["categories"] = await self._sanitize_categories(
                cast(StoreID, store.id), update_dict["categories"]
            )

        for field, value in update_dict.items():
            setattr(product, field, value)

        try:
            await product.save()
        except DuplicateKeyError as exc:
            raise_for_duplicate_key(exc)
        logger.info(f"Updated product {product_id} for store {store.id}")
        return Product.model_validate(product)

    async def delete_product(self, store_id: str, product_id: str) -> bool:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return False

        product = await ProductModel.find(
            {**parse_ref(product_id), "store_id": store.id, "deleted_at": None}
        ).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return False

        now = pendulum.now()

        # Soft delete all variants of this product
        variants_result = await VariantModel.find({"product_id": product.id, "deleted_at": None}).update_many(
            {"$set": {"deleted_at": now}}
        )
        logger.info(f"Soft deleted {getattr(variants_result, 'modified_count', 0)} variants for product {product_id}")

        # Delete the product itself
        product.deleted_at = now
        await product.save()
        logger.info(f"Deleted product {product_id} for store {store.id}")
        return True
