from typing import cast

# from uuid import uuid7
import pendulum

from src.core.logging import logger
from src.domain.types.bundles import Bundle, BundleID, NewBundle, UpdateBundle
from src.domain.types.categories import CategoryID
from src.domain.types.locations import LocationID
from src.domain.types.prices import LocationPriceMap
from src.domain.types.stores import StoreID
from src.domain.types.variants import VariantID
from src.models.bundles import BundleModel
from src.models.categories import CategoryModel
from src.models.locations import LocationModel
from src.models.stores import StoreModel
from src.models.variants import VariantModel


class BundlesService:
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

    async def _sanitize_components(self, store_id: StoreID, component_ids: list[VariantID]) -> list[VariantID]:
        """Filter component IDs to only include valid variant IDs that exist and belong to the specified store."""
        if not component_ids:
            return []

        # Get all variants in one query
        variants = await VariantModel.find(
            {"_id": {"$in": component_ids}, "store_id": store_id, "deleted_at": None}
        ).to_list()

        # Return only valid variant IDs
        valid_ids: list[VariantID] = [cast(VariantID, var.id) for var in variants]

        # Log if any components were filtered out
        if len(valid_ids) != len(component_ids):
            found_ids = {str(var.id) for var in variants}
            requested_ids = {str(comp_id) for comp_id in component_ids}
            filtered_ids = requested_ids - found_ids
            logger.info(
                f"Filtered out invalid components for store {store_id}: {filtered_ids}. "
                f"Kept {len(valid_ids)} valid components."
            )

        return valid_ids

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

    async def create_bundle(self, store_id: StoreID, new_bundle: NewBundle) -> Bundle | None:
        """Create a new bundle in the specified store.

        Args:
            store_id: The UUID of the store where the bundle will be created.
            new_bundle: The bundle data to create.

        Returns:
            The created Bundle object, or None if the store doesn't exist.

        """
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        # Sanitize categories - keep only valid ones
        valid_categories = None
        if new_bundle.categories is not None:
            valid_categories = await self._sanitize_categories(store_id, new_bundle.categories)

        # Sanitize components - keep only valid ones
        valid_components = None
        if new_bundle.components is not None:
            valid_components = await self._sanitize_components(store_id, new_bundle.components)

        # Sanitize location_price - keep only valid locations
        valid_location_price = await self._sanitize_location_prices(store_id, new_bundle.location_price)

        bundle = BundleModel(
            # id=uuid7(),
            store_id=store_id,
            name=new_bundle.name,
            description=new_bundle.description,
            components=valid_components,
            attributes=new_bundle.attributes if new_bundle.attributes is not None else {},
            categories=valid_categories,
            price=new_bundle.price,
            location_price=valid_location_price,
            region_price=new_bundle.region_price,
            images=new_bundle.images,
        )
        bundle = await bundle.create()
        logger.info(f"Created bundle {bundle.id} for store {store_id}")

        return Bundle.model_validate(bundle.model_dump())

    async def list_bundles(self, store_id: StoreID) -> list[Bundle] | None:
        """List all non-deleted bundles for a specific store.

        Args:
            store_id: The UUID of the store.

        Returns:
            A list of Bundle objects, or None if the store doesn't exist.

        """
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        bundles = await BundleModel.find({"store_id": store_id, "deleted_at": None}).to_list()
        logger.debug(f"Found {len(bundles)} bundles for store {store_id}")
        return [Bundle.model_validate(bundle.model_dump()) for bundle in bundles]

    async def get_bundle(self, store_id: StoreID, bundle_id: BundleID) -> Bundle | None:
        """Get a specific bundle by ID from a store.

        Args:
            store_id: The UUID of the store.
            bundle_id: The UUID of the bundle to retrieve.

        Returns:
            The Bundle object if found and belongs to the store, None otherwise.

        """
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        bundle = await BundleModel.find({"_id": bundle_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if bundle:
            return Bundle.model_validate(bundle.model_dump())
        logger.warning(f"Bundle not found or access denied: bundle_id={bundle_id}, store_id={store_id}")
        return None

    async def update_bundle(
        self,
        store_id: StoreID,
        bundle_id: BundleID,
        update_data: UpdateBundle,
    ) -> Bundle | None:
        """Update an existing bundle's information.

        Args:
            store_id: The UUID of the store.
            bundle_id: The UUID of the bundle to update.
            update_data: The partial bundle data to update.

        Returns:
            The updated Bundle object, or None if not found or access denied.

        """
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return None

        bundle = await BundleModel.find({"_id": bundle_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not bundle:
            logger.warning(f"Bundle not found or access denied: bundle_id={bundle_id}, store_id={store_id}")
            return None

        # Update only fields that were explicitly set
        update_dict = update_data.model_dump(exclude_unset=True)

        # Sanitize categories if they are being updated
        if "categories" in update_dict and update_dict["categories"] is not None:
            update_dict["categories"] = await self._sanitize_categories(store_id, update_dict["categories"])

        # Sanitize components if they are being updated
        if "components" in update_dict and update_dict["components"] is not None:
            update_dict["components"] = await self._sanitize_components(store_id, update_dict["components"])

        # Sanitize location_price if it is being updated
        if "location_price" in update_dict:
            update_dict["location_price"] = await self._sanitize_location_prices(
                store_id, update_dict["location_price"]
            )

        for field, value in update_dict.items():
            setattr(bundle, field, value)

        await bundle.save()
        logger.info(f"Updated bundle {bundle_id} for store {store_id}")
        return Bundle.model_validate(bundle.model_dump())

    async def delete_bundle(self, store_id: StoreID, bundle_id: BundleID) -> bool:
        """Soft delete a bundle by setting its deleted_at timestamp.

        Args:
            store_id: The UUID of the store.
            bundle_id: The UUID of the bundle to delete.

        Returns:
            True if the bundle was successfully deleted, False otherwise.

        """
        # Check if store exists
        store = await StoreModel.find({"_id": store_id, "deleted_at": None}).first_or_none()
        if not store:
            logger.warning(f"Store not found: {store_id}")
            return False

        bundle = await BundleModel.find({"_id": bundle_id, "store_id": store_id, "deleted_at": None}).first_or_none()
        if not bundle:
            logger.warning(f"Bundle not found or access denied: bundle_id={bundle_id}, store_id={store_id}")
            return False

        bundle.deleted_at = pendulum.now()
        await bundle.save()
        logger.info(f"Deleted bundle {bundle_id} for store {store_id}")
        return True
