from pymongo import IndexModel

from src.core.utils import split_path
from src.domain.types.attributes import AttributesMap
from src.domain.types.categories import (
    CategoryDescription,
    CategoryImages,
    CategoryName,
    CategoryPath,
    CategorySEO,
    CategoryStatus,
    CategoryUUID,
)
from src.domain.types.stores import StoreUUID
from src.models.base import BaseAppDocument


class CategoryModel(BaseAppDocument):
    id: CategoryUUID  # type: ignore
    store_id: StoreUUID
    name: CategoryName
    description: CategoryDescription | None = None
    status: CategoryStatus
    seo: CategorySEO | None = None
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
        ]

    @classmethod
    def parse_path(cls, path: CategoryPath) -> list[str]:
        return split_path(path)
