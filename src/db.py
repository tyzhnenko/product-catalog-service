from contextlib import asynccontextmanager

from beanie import Document, init_beanie
from fastapi import FastAPI
from pymongo import AsyncMongoClient

from src.core.types import FastAPIServices
from src.models.categories import CategoryModel
from src.models.locations import LocationModel
from src.models.products import ProductModel
from src.models.stores import StoreModel
from src.models.variants import VariantModel
from src.settings import Settings

DOCUMENT_MODELS: list[type[Document]] = [
    StoreModel,
    CategoryModel,
    LocationModel,
    ProductModel,
    VariantModel,
]


async def init_db(settings: Settings) -> AsyncMongoClient:
    # Create Motor client
    driver: str = settings.db.driver
    host: str = settings.db.host
    user: str | None = settings.db.user
    password: str | None = settings.db.password
    port: int = settings.db.port
    database: str = settings.db.database
    client: AsyncMongoClient

    connect_string: str = f"{driver}://"
    if user and password:
        connect_string += f"{user}:{password}@"
    connect_string += f"{host}:{port}/{database}"

    client = AsyncMongoClient(
        connect_string,
        uuidRepresentation="standard",
        tz_aware=True,
    )

    await init_beanie(
        database=getattr(client, database),
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
