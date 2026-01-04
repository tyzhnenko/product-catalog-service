from pymongo import IndexModel

from src.domain.types.attributes import AttributesMap
from src.domain.types.locations import LocationName, LocationUUID
from src.domain.types.stores import StoreUUID
from src.models.base import BaseAppDocument


class LocationModel(BaseAppDocument):
    id: LocationUUID  # type: ignore
    name: LocationName
    store_id: StoreUUID
    attributes: AttributesMap

    class Settings:
        name = "locations"
        indexes: list[IndexModel] = [
            IndexModel(["name"], unique=True),
            IndexModel(["store_id", "deleted_at"]),  # Optimize list queries with soft delete filtering
            IndexModel(
                ["attributes.$**"],
                name="attributes_wildcard_idx",
            ),
        ]
