# from uuid import uuid7

from typing import cast, overload

import pendulum
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from src.core.fields import FieldSelection, projection_model, to_partial
from src.core.logging import logger
from src.core.pagination import PaginationParams
from src.core.types import PaginatedResponse
from src.core.utils import paginate, parse_ref, raise_for_duplicate_key
from src.domain.types.categories import CategoryID
from src.domain.types.products import (
    NewProduct,
    PartialProduct,
    Product,
    ProductID,
    ProductStatusEnum,
    UpdateProduct,
)
from src.domain.types.stores import StoreID
from src.domain.types.variants import PartialProductWithVariants, ProductVariant, ProductWithVariants
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

    async def _fetch_variants_by_product(
        self, store_id: StoreID, product_ids: list[ProductID]
    ) -> dict[ProductID, list[ProductVariant]]:
        """Batch-fetch non-deleted variants for a set of products, grouped by product_id."""
        if not product_ids:
            return {}

        variants = await VariantModel.find(
            {"store_id": store_id, "product_id": {"$in": product_ids}, "deleted_at": None}
        ).to_list()

        grouped: dict[ProductID, list[ProductVariant]] = {}
        for variant in variants:
            grouped.setdefault(variant.product_id, []).append(ProductVariant.model_validate(variant))
        return grouped

    def _with_variants(
        self, product: Product | PartialProduct, variants: list[ProductVariant]
    ) -> ProductWithVariants | PartialProductWithVariants:
        """Attach embedded variants to a `Product`/`PartialProduct`, preserving `fields`-narrowed unset tracking."""
        target_cls = PartialProductWithVariants if isinstance(product, PartialProduct) else ProductWithVariants
        return target_cls.model_validate({**product.model_dump(exclude_unset=True), "variants": variants})

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

    @overload
    async def list_products(
        self,
        store_id: str,
        pagination: PaginationParams,
        filters: dict | None = None,
        variant_filters: dict | None = None,
        fields: None = None,
        include_variants: bool = False,
    ) -> PaginatedResponse[Product] | None: ...

    @overload
    async def list_products(
        self,
        store_id: str,
        pagination: PaginationParams,
        filters: dict | None = None,
        variant_filters: dict | None = None,
        fields: FieldSelection = ...,
        include_variants: bool = False,
    ) -> PaginatedResponse[PartialProduct] | None: ...

    async def list_products(
        self,
        store_id: str,
        pagination: PaginationParams,
        filters: dict | None = None,
        variant_filters: dict | None = None,
        fields: FieldSelection | None = None,
        include_variants: bool = False,
    ) -> PaginatedResponse[Product] | PaginatedResponse[PartialProduct] | None:
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

        result: PaginatedResponse[Product] | PaginatedResponse[PartialProduct]
        if fields:
            result = await paginate(
                ProductModel.find(query_filter).project(projection_model(Product, fields.fetch_names(Product))),
                pagination.after,
                pagination.before,
                pagination.limit,
                transform=lambda doc: to_partial(PartialProduct, doc, fields),
            )
        else:
            result = await paginate(
                ProductModel.find(query_filter),
                pagination.after,
                pagination.before,
                pagination.limit,
                transform=Product.model_validate,
            )

        if not include_variants or not result.items:
            return result

        variants_by_product = await self._fetch_variants_by_product(
            cast(StoreID, store.id), [item.id for item in result.items]
        )
        new_items = [self._with_variants(item, variants_by_product.get(item.id, [])) for item in result.items]
        item_type = type(new_items[0])
        return PaginatedResponse[item_type](  # type: ignore[valid-type]
            items=new_items,
            start_cursor=result.start_cursor,
            end_cursor=result.end_cursor,
            has_next=result.has_next,
            has_prev=result.has_prev,
            total=result.total,
        )

    @overload
    async def get_product(
        self, store_id: str, product_id: str, fields: None = None, include_variants: bool = False
    ) -> Product | None: ...

    @overload
    async def get_product(
        self, store_id: str, product_id: str, fields: FieldSelection = ..., include_variants: bool = False
    ) -> PartialProduct | None: ...

    async def get_product(
        self,
        store_id: str,
        product_id: str,
        fields: FieldSelection | None = None,
        include_variants: bool = False,
    ) -> Product | PartialProduct | None:
        # Check if store exists
        store = await StoreModel.find({**parse_ref(store_id), "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        query = ProductModel.find({**parse_ref(product_id), "store_id": store.id, "deleted_at": None})
        product: Product | PartialProduct | None = None
        if fields:
            doc = await query.project(projection_model(Product, fields.fetch_names(Product))).first_or_none()
            if doc:
                product = to_partial(PartialProduct, doc, fields)
        else:
            doc = await query.first_or_none()
            if doc:
                product = Product.model_validate(doc)

        if product is None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        if not include_variants:
            return product

        variants_by_product = await self._fetch_variants_by_product(cast(StoreID, store.id), [product.id])
        return self._with_variants(product, variants_by_product.get(product.id, []))

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
