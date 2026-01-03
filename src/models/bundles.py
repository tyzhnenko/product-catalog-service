from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.bundles import (
    BundleCategories,
    BundleComponents,
    BundleDescription,
    BundleName,
    BundleUUID,
)
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap
from src.domain.types.stores import StoreUUID
from src.models.base import BaseAppDocument


class BundleModel(BaseAppDocument):
    id: BundleUUID  # type: ignore
    store_id: StoreUUID
    name: BundleName
    description: BundleDescription | None
    components: BundleComponents | None
    attributes: AttributesMap
    categories: BundleCategories | None
    price: PriceMap | None
    location_price: LocationPriceMap | None
    region_price: RegionPriceMap | None

    class Settings:
        name = "bundles"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "deleted_at"]),
            IndexModel(
                ["store_id", "attributes.$**", "deleted_at"],
                name="store_attributes_index",
            ),
            IndexModel(
                ["store_id", "price.$**"],
                name="store_price_wildcard_idx",
            ),
            IndexModel(
                ["store_id", "location_price.$**"],
                name="store_location_price_wildcard_idx",
            ),
            IndexModel(
                ["store_id", "region_price.$**"],
                name="store_region_price_wildcard_idx",
            ),
        ]
