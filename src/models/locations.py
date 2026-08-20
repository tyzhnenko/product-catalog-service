from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.locations import LocationName
from src.domain.types.seo import SEO
from src.domain.types.stores import StoreID
from src.models.base import BaseAppDocument


class LocationModel(BaseAppDocument):
    name: LocationName
    store_id: StoreID
    attributes: AttributesMap
    seo: SEO | None = None

    class Settings:
        name = "locations"
        indexes: list[IndexModel] = [
            IndexModel(["store_id", "name"], unique=True),
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
