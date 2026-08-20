from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field

from src.domain.types.base import HTTPURLField
from src.domain.types.refs import ObjectIdRef, SlugRef
from src.domain.types.seo import SEO

type StoreID = Annotated[
    PydanticObjectId,
    Field(
        ...,
        title="Store ID",
        description="Unique identifier for a store",
    ),
]

type StoreRef = Annotated[
    ObjectIdRef | SlugRef,
    Field(
        title="Store Ref",
        description="Store ID or slug ref (prefixed 's-')",
    ),
]

type StoreName = Annotated[
    str,
    Field(
        ...,
        title="Store Name",
        min_length=1,
        max_length=256,
        description="Name of the store",
    ),
]


class NewStore(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: StoreName
    url: HTTPURLField
    seo: SEO | None = None


class Store(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: StoreID
    name: StoreName
    url: HTTPURLField
    seo: SEO | None = None


class UpdateStore(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: StoreName | None = None
    url: HTTPURLField | None = None
    seo: SEO | None = None
