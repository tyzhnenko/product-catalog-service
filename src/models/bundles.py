from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.bundles import (
    BundleCategories,
    BundleComponents,
    BundleDescription,
    BundleImages,
    BundleName,
)
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap
from src.domain.types.seo import SEO
from src.domain.types.stores import StoreID
from src.models.base import BaseAppDocument


class BundleModel(BaseAppDocument):
    store_id: StoreID
    name: BundleName
    description: BundleDescription | None
    components: BundleComponents | None
    attributes: AttributesMap
    categories: BundleCategories | None
    price: PriceMap | None
    location_price: LocationPriceMap | None
    region_price: RegionPriceMap | None
    images: BundleImages | None = None
    seo: SEO | None = None

    class Settings:
        name = "bundles"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "deleted_at"]),
            IndexModel(
                ["attributes.$**"],
                name="attributes_wildcard_idx",
            ),
            IndexModel(
                ["price.$**"],
                name="price_wildcard_idx",
            ),
            IndexModel(
                ["location_price.$**"],
                name="location_price_wildcard_idx",
            ),
            IndexModel(
                ["region_price.$**"],
                name="region_price_wildcard_idx",
            ),
            IndexModel(
                ["store_id", "seo.slug"],
                unique=True,
                partialFilterExpression={"seo.slug": {"$exists": True}},
            ),
        ]
