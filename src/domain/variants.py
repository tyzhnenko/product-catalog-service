from uuid import uuid7

import pendulum

from src.core.logging import logger
from src.domain.types.products import ProductUUID
from src.domain.types.stores import StoreUUID
from src.domain.types.variants import (
    NewProductVariant,
    ProductVariant,
    UpdateProductVariant,
    VariantUUID,
)
from src.models.products import ProductModel
from src.models.variants import VariantModel


class VariantsService:
    async def create_variant(
        self, store_id: StoreUUID, product_id: ProductUUID, new_variant: NewProductVariant
    ) -> ProductVariant | None:
        # Check if product exists and belongs to the store (product query validates store ownership)
        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variant = VariantModel(
            id=uuid7(),
            store_id=store_id,
            product_id=product_id,
            title=new_variant.title,
            sku=new_variant.sku,
            upc=new_variant.upc,
            ean=new_variant.ean,
            jan=new_variant.jan,
            isbn=new_variant.isbn,
            options=new_variant.options,
            attributes=new_variant.attributes or {},
        )
        variant = await variant.create()
        logger.info(f"Created variant {variant.id} for product {product_id}")

        return ProductVariant.model_validate(variant)

    async def list_variants(self, store_id: StoreUUID, product_id: ProductUUID) -> list[ProductVariant] | None:
        # Check if product exists and belongs to the store
        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variants = await VariantModel.find(
            {"product_id": product_id, "store_id": store_id, "deleted_at": None}
        ).to_list()
        logger.debug(f"Found {len(variants)} variants for product {product_id}")
        return [ProductVariant.model_validate(variant) for variant in variants]

    async def get_variant(
        self, store_id: StoreUUID, product_id: ProductUUID, variant_id: VariantUUID
    ) -> ProductVariant | None:
        # Check if product exists and belongs to the store
        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variant = await VariantModel.get(variant_id)
        if variant and variant.product_id == product_id and variant.store_id == store_id and variant.deleted_at is None:
            return ProductVariant.model_validate(variant)
        logger.warning(f"Variant not found or access denied: variant_id={variant_id}, product_id={product_id}")
        return None

    async def update_variant(
        self,
        store_id: StoreUUID,
        product_id: ProductUUID,
        variant_id: VariantUUID,
        update_data: UpdateProductVariant,
    ) -> ProductVariant | None:
        # Check if product exists and belongs to the store
        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variant = await VariantModel.get(variant_id)
        if (
            not variant
            or variant.product_id != product_id
            or variant.store_id != store_id
            or variant.deleted_at is not None
        ):
            logger.warning(f"Variant not found or access denied: variant_id={variant_id}, product_id={product_id}")
            return None

        # Update only fields that were explicitly set
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(variant, field, value)

        await variant.save()
        logger.info(f"Updated variant {variant_id} for product {product_id}")
        return ProductVariant.model_validate(variant)

    async def delete_variant(self, store_id: StoreUUID, product_id: ProductUUID, variant_id: VariantUUID) -> bool:
        # Check if product exists and belongs to the store
        product = await ProductModel.get(product_id)
        if not product or product.store_id != store_id or product.deleted_at is not None:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return False

        variant = await VariantModel.get(variant_id)
        if (
            not variant
            or variant.product_id != product_id
            or variant.store_id != store_id
            or variant.deleted_at is not None
        ):
            logger.warning(f"Variant not found or access denied: variant_id={variant_id}, product_id={product_id}")
            return False

        variant.deleted_at = pendulum.now()
        await variant.save()
        logger.info(f"Deleted variant {variant_id} for product {product_id}")
        return True
