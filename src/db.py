from contextlib import asynccontextmanager
from urllib.parse import quote_plus, urlencode

from beanie import Document, init_beanie
from fastapi import FastAPI
from pymongo import AsyncMongoClient

from src.core.types import FastAPIServices
from src.models.bundles import BundleModel
from src.models.categories import CategoryModel
from src.models.locations import LocationModel
from src.models.products import ProductModel
from src.models.stores import StoreModel
from src.models.variants import VariantModel
from src.settings import Database, Settings

DOCUMENT_MODELS: list[type[Document]] = [
    StoreModel,
    CategoryModel,
    LocationModel,
    ProductModel,
    VariantModel,
    BundleModel,
]


def build_connection_string(db: Database) -> str:
    connect_string = f"{db.driver}://"
    if db.user and db.password:
        # pymongo unquotes credentials with unquote_plus, so quote_plus is the matching escape
        connect_string += f"{quote_plus(db.user)}:{quote_plus(db.password)}@"
    connect_string += f"{db.host}:{db.port}/{db.database}"

    params: dict[str, str] = {}
    if db.auth_source:
        params["authSource"] = db.auth_source
    if db.tls:
        params["tls"] = "true"
    if params:
        connect_string += f"?{urlencode(params)}"

    return connect_string


async def init_db(settings: Settings) -> AsyncMongoClient:
    client: AsyncMongoClient = AsyncMongoClient(
        build_connection_string(settings.db),
        uuidRepresentation="standard",
        tz_aware=True,
    )

    await init_beanie(
        database=getattr(client, settings.db.database),
        document_models=DOCUMENT_MODELS,
    )

    return client


def use_beanie(services: FastAPIServices, settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        client = await init_db(settings)
        yield
        await client.close()

    services.add_lifespan(lifespan)
