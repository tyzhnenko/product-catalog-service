from pymongo import IndexModel

from src.domain.types.base import URLField
from src.domain.types.stores import StoreName, StoreUUID
from src.models.base import BaseAppDocument


class StoreModel(BaseAppDocument):
    id: StoreUUID  # pyright: ignore[reportIncompatibleVariableOverride,reportGeneralTypeIssues]
    name: StoreName
    url: URLField

    class Settings:
        name = "stores"
        indexes: list[IndexModel] = [
            IndexModel(["name"], unique=True),
        ]
