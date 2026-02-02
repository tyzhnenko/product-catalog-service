from typing import cast

# from uuid import uuid7
import pendulum

from src.core.logging import logger
from src.domain.types.locations import LocationID
from src.domain.types.prices import LocationPriceMap
from src.domain.types.products import ProductID
from src.domain.types.stores import StoreID
from src.domain.types.variants import (
    NewProductVariant,
    ProductVariant,
    UpdateProductVariant,
    VariantID,
)
from src.models.locations import LocationModel
from src.models.products import ProductModel
from src.models.variants import VariantModel


class DuplicateVariantOptionsError(Exception):
    """Raised when attempting to create/update a variant with duplicate options."""

    pass


class VariantsService:
    async def _check_duplicate_options(
        self,
        product_id: ProductID,
        store_id: StoreID,
        options: list,
        exclude_variant_id: VariantID | None = None,
    ) -> bool:
        """Check if a variant with the same options already exists for the product.

        Args:
            product_id: The product ID to check within
            store_id: The store ID
            options: The options list to check for duplicates
            exclude_variant_id: Optional variant ID to exclude from check (for updates)

        Returns:
            True if duplicate options found, False otherwise

        """
        # Build the query filter
        query_filter: dict = {
            "product_id": product_id,
            "store_id": store_id,
            "deleted_at": None,
        }

        if exclude_variant_id:
            query_filter["_id"] = {"$ne": exclude_variant_id}

        # Get all variants for this product
        variants = await VariantModel.find(query_filter).to_list()

        # Convert the input options to a comparable format (sorted list of tuples)
        # Handle both VariantOption objects and dicts (from API updates)
        if not options:
            # Empty options list
            input_options_normalized = []
        elif isinstance(options[0], dict):
            # Dict format (from API updates)
            input_options_normalized = sorted([(opt["name"], opt["value"]) for opt in options])
        else:
            # VariantOption objects
            input_options_normalized = sorted([(opt.name, opt.value) for opt in options])

        # Check each existing variant's options
        for variant in variants:
            variant_options_normalized = sorted([(opt.name, opt.value) for opt in variant.options])
            if variant_options_normalized == input_options_normalized:
                logger.info(
                    f"Duplicate options found for product {product_id}: "
                    f"variant {variant.id} already has options {variant_options_normalized}"
                )
                return True

        return False

    async def _sanitize_location_prices(
        self, store_id: StoreID, location_price: LocationPriceMap | None
    ) -> LocationPriceMap | None:
        """Filter location_price to only include valid location IDs that exist and belong to the specified store."""
        if not location_price:
            return location_price

        location_ids = list(location_price.keys())

        # Get all locations in one query
        locations = await LocationModel.find(
            {"_id": {"$in": location_ids}, "store_id": store_id, "deleted_at": None}
        ).to_list()

        # Create a set of valid location IDs using their native type (e.g., UUID7)
        valid_location_ids = {cast(LocationID, loc.id) for loc in locations}

        # Filter location_price to only include valid locations
        sanitized_location_price = {
            loc_id: prices for loc_id, prices in location_price.items() if loc_id in valid_location_ids
        }

        # Log if any locations were filtered out
        if len(sanitized_location_price) != len(location_price):
            requested_ids = set(location_price.keys())
            filtered_ids = requested_ids - valid_location_ids
            logger.info(
                f"Filtered out invalid locations for store {store_id}: {filtered_ids}. "
                f"Kept {len(sanitized_location_price)} valid locations."
            )

        return sanitized_location_price if sanitized_location_price else None

    async def create_variant(
        self, store_id: StoreID, product_id: ProductID, new_variant: NewProductVariant
    ) -> ProductVariant | None:
        # Check if product exists and belongs to the store (product query validates store ownership)
        product = await ProductModel.find({"_id": product_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        # Check for duplicate options within the product
        if await self._check_duplicate_options(product_id, store_id, new_variant.options):
            raise DuplicateVariantOptionsError(f"A variant with these options already exists for product {product_id}")

        # Sanitize location_price - keep only valid locations
        valid_location_price = await self._sanitize_location_prices(store_id, new_variant.location_price)

        variant = VariantModel(
            # id=uuid7(),
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
            price=new_variant.price,
            location_price=valid_location_price,
            region_price=new_variant.region_price,
            images=new_variant.images,
        )
        variant = await variant.create()
        logger.info(f"Created variant {variant.id} for product {product_id}")

        return ProductVariant.model_validate(variant)

    async def list_variants(self, store_id: StoreID, product_id: ProductID) -> list[ProductVariant] | None:
        # Check if product exists and belongs to the store
        product = await ProductModel.find({"_id": product_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variants = await VariantModel.find(
            {"product_id": product_id, "store_id": store_id, "deleted_at": None}
        ).to_list()
        logger.debug(f"Found {len(variants)} variants for product {product_id}")
        return [ProductVariant.model_validate(variant) for variant in variants]

    async def get_variant(
        self, store_id: StoreID, product_id: ProductID, variant_id: VariantID
    ) -> ProductVariant | None:
        # Check if product exists and belongs to the store
        product = await ProductModel.find({"_id": product_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variant = await VariantModel.find(
            {"_id": variant_id, "product_id": product_id, "store_id": store_id, "deleted_at": None}
        ).first_or_none()
        if variant:
            return ProductVariant.model_validate(variant)
        logger.warning(f"Variant not found or access denied: variant_id={variant_id}, product_id={product_id}")
        return None

    async def update_variant(
        self,
        store_id: StoreID,
        product_id: ProductID,
        variant_id: VariantID,
        update_data: UpdateProductVariant,
    ) -> ProductVariant | None:
        # Check if product exists and belongs to the store
        product = await ProductModel.find({"_id": product_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return None

        variant = await VariantModel.find(
            {"_id": variant_id, "product_id": product_id, "store_id": store_id, "deleted_at": None}
        ).first_or_none()
        if not variant:
            logger.warning(f"Variant not found or access denied: variant_id={variant_id}, product_id={product_id}")
            return None

        # Update only fields that were explicitly set
        update_dict = update_data.model_dump(exclude_unset=True)

        # Check for duplicate options if options are being updated
        if "options" in update_dict:
            if await self._check_duplicate_options(
                product_id, store_id, update_dict["options"], exclude_variant_id=variant_id
            ):
                raise DuplicateVariantOptionsError(
                    f"A variant with these options already exists for product {product_id}"
                )

        # Sanitize location_price if it's being updated
        if "location_price" in update_dict:
            update_dict["location_price"] = await self._sanitize_location_prices(
                store_id, update_dict["location_price"]
            )

        for field, value in update_dict.items():
            setattr(variant, field, value)

        await variant.save()
        logger.info(f"Updated variant {variant_id} for product {product_id}")
        return ProductVariant.model_validate(variant)

    async def delete_variant(self, store_id: StoreID, product_id: ProductID, variant_id: VariantID) -> bool:
        # Check if product exists and belongs to the store
        product = await ProductModel.find({"_id": product_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not product:
            logger.warning(f"Product not found or access denied: product_id={product_id}, store_id={store_id}")
            return False

        variant = await VariantModel.find(
            {"_id": variant_id, "product_id": product_id, "store_id": store_id, "deleted_at": None}
        ).first_or_none()
        if not variant:
            logger.warning(f"Variant not found or access denied: variant_id={variant_id}, product_id={product_id}")
            return False

        variant.deleted_at = pendulum.now()
        await variant.save()
        logger.info(f"Deleted variant {variant_id} for product {product_id}")
        return True
