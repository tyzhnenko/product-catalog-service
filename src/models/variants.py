from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.prices import PriceMap
from src.domain.types.products import ProductUUID
from src.domain.types.stores import StoreUUID
from src.domain.types.variants import (
    VariantEAN,
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

    class Settings:
        name = "variants"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "product_id", "deleted_at"]),
            IndexModel(
                ["store_id", "attributes.$**", "deleted_at"],
                name="store_attributes_index",
            ),
            IndexModel(
                ["store_id", "price.$**"],
                name="store_price_wildcard_idx",
            ),
        ]
