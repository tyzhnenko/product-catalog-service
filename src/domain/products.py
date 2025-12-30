from uuid import uuid7

import pendulum

from src.core.logging import logger
from src.domain.types.products import (
    NewProduct,
    Product,
    ProductStatusEnum,
    ProductUUID,
    UpdateProduct,
)
from src.domain.types.stores import StoreUUID
from src.models.products import ProductModel
from src.models.stores import StoreModel


class ProductsService:
    async def create_product(self, store_id: StoreUUID, new_product: NewProduct) -> Product | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        product = ProductModel(
            id=uuid7(),
            store_id=store_id,
            name=new_product.name,
            description=new_product.description,
            tags=new_product.tags,
            seo=new_product.seo,
            status=ProductStatusEnum.ACTIVE,
            attributes=[],
        )
        product = await product.create()
        logger.info(f"Created product {product.id} for store {store_id}")

        return Product.model_validate(product)

    async def list_products(self, store_id: StoreUUID) -> list[Product] | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        products = await ProductModel.find({"store_id": store_id, "deleted_at": None}).to_list()
        logger.debug(f"Found {len(products)} products for store {store_id}")
        return [Product.model_validate(product) for product in products]

    async def get_product(self, store_id: StoreUUID, product_id: ProductUUID) -> Product | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        product = await ProductModel.get(product_id)
        if product and product.store_id == store_id and product.deleted_at is None:
            return Product.model_validate(product)
        logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
        return None

    async def update_product(
        self,
        store_id: StoreUUID,
        product_id: ProductUUID,
        update_data: UpdateProduct,
    ) -> Product | None:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        # Update only fields that were explicitly set
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(product, field, value)

        await product.save()
        logger.info(f"Updated product {product_id} for store {store_id}")
        return Product.model_validate(product)

    async def delete_product(self, store_id: StoreUUID, product_id: ProductUUID) -> bool:
        # Check if store exists
        store = await StoreModel.get(store_id)
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return False

        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return False

        product.deleted_at = pendulum.now()
        await product.save()
        logger.info(f"Deleted product {product_id} for store {store_id}")
        return True
