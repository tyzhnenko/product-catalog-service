from pymongo import IndexModel

from src.core.utils import split_path
from src.domain.types.attributes import AttributesMap
from src.domain.types.categories import (
    CategoryDescription,
    CategoryImages,
    CategoryName,
    CategoryPath,
    CategoryStatus,
)
from src.domain.types.seo import SEO
from src.domain.types.stores import StoreID
from src.models.base import BaseAppDocument


class CategoryModel(BaseAppDocument):
    store_id: StoreID
    name: CategoryName
    description: CategoryDescription | None = None
    status: CategoryStatus
    seo: SEO | None = None
    path: CategoryPath
    paths: list[str] = []
    attributes: AttributesMap
    images: CategoryImages | None = None

    class Settings:
        name = "categories"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "deleted_at"]),  # Optimize list queries with soft delete filtering
            IndexModel(["store_id", "path", "deleted_at"]),
            IndexModel(["store_id", "paths", "deleted_at"]),
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

    @classmethod
    def parse_path(cls, path: CategoryPath) -> list[str]:
        return split_path(path)
