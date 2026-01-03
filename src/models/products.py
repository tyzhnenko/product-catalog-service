from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.products import (
    ProductDescription,
    ProductName,
    ProductSEO,
    ProductStatus,
    ProductTags,
    ProductUUID,
)
from src.domain.types.stores import StoreUUID
from src.models.base import BaseAppDocument


class ProductModel(BaseAppDocument):
    id: ProductUUID  # type: ignore
    store_id: StoreUUID
    name: ProductName
    description: ProductDescription | None = None
    tags: ProductTags
    status: ProductStatus
    seo: ProductSEO | None = None
    attributes: AttributesMap

    class Settings:
        name = "products"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "deleted_at"]),  # Optimize list queries with soft delete filtering
        ]
