from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.categories import CategoryID
from src.domain.types.products import (
    ProductBrand,
    ProductDescription,
    ProductName,
    ProductStatus,
    ProductTags,
)
from src.domain.types.seo import SEO
from src.domain.types.stores import StoreID
from src.models.base import BaseAppDocument


class ProductModel(BaseAppDocument):
    store_id: StoreID
    name: ProductName
    description: ProductDescription | None = None
    brand: ProductBrand | None = None
    tags: ProductTags
    status: ProductStatus
    seo: SEO | None = None
    attributes: AttributesMap
    categories: list[CategoryID] = []

    class Settings:
        name = "products"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "deleted_at"]),  # Optimize list queries with soft delete filtering
            IndexModel(
                ["attributes.$**"],
                name="attributes_wildcard_idx",
            ),
            IndexModel(
                ["store_id", "seo.slug"],
                unique=True,
                partialFilterExpression={"seo.slug": {"$exists": True}},
            ),
        ]
