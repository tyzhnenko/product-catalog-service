from pymongo import IndexModel

from src.domain.types.base import HTTPURLField
from src.domain.types.stores import StoreName, StoreUUID
from src.models.base import BaseAppDocument


class StoreModel(BaseAppDocument):
    id: StoreUUID  # type: ignore
    name: StoreName
    url: HTTPURLField

    class Settings:
        name = "stores"
        indexes: list[IndexModel] = [
            IndexModel(["name"], unique=True),
        ]
