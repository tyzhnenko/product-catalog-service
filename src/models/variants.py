from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap
from src.domain.types.products import ProductUUID
from src.domain.types.stores import StoreUUID
from src.domain.types.variants import (
    VariantEAN,
    VariantImages,
    VariantISBN,
    VariantJAN,
    VariantOptions,
    VariantSKU,
    VariantTitle,
    VariantUPC,
    VariantUUID,
)
from src.models.base import BaseAppDocument


class VariantModel(BaseAppDocument):
    id: VariantUUID  # type: ignore
    store_id: StoreUUID
    product_id: ProductUUID
    title: VariantTitle
    sku: VariantSKU | None
    upc: VariantUPC | None
    ean: VariantEAN | None
    jan: VariantJAN | None
    isbn: VariantISBN | None
    attributes: AttributesMap
    options: VariantOptions
    price: PriceMap | None
    location_price: LocationPriceMap | None
    region_price: RegionPriceMap | None
    images: VariantImages | None = None

    class Settings:
        name = "variants"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "product_id", "deleted_at"]),
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
        ]
