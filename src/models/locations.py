from pymongo import IndexModel

from src.domain.types.locations import LocationName, LocationUUID
from src.domain.types.stores import StoreUUID
from src.models.base import BaseAppDocument


class LocationModel(BaseAppDocument):
    id: LocationUUID  # type: ignore
    name: LocationName
    store_id: StoreUUID

    class Settings:
        name = "locations"
        indexes: list[IndexModel] = [
            IndexModel(["name"], unique=True),
        ]
