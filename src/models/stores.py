from pymongo import IndexModel

from src.domain.types.base import HTTPURLField
from src.domain.types.seo import SEO
from src.domain.types.stores import StoreName
from src.models.base import BaseAppDocument


class StoreModel(BaseAppDocument):
    name: StoreName
    url: HTTPURLField
    seo: SEO | None = None

    class Settings:
        name = "stores"
        indexes: list[IndexModel] = [
            IndexModel(["name"], unique=True),
            IndexModel(
                ["seo.slug"],
                unique=True,
                partialFilterExpression={"seo.slug": {"$exists": True}},
            ),
        ]
