from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field

from src.domain.types.base import URLField

StoreUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a store",
        json_schema_extra={
            "format": "uuid",
        },
    ),
]

StoreName = Annotated[
    str,
    Field(
        ...,
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
    url: URLField


class Store(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: StoreUUID
    name: StoreName
    url: URLField


class UpdateStore(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: StoreName | None = None
    url: URLField | None = None
