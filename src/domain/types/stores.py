from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field

from src.domain.types.base import HTTPURLField

type StoreUUID = Annotated[
    UUID7,
    Field(
        ...,
        title="Store UUID",
        description="Unique identifier for a store",
        json_schema_extra={
            "format": "uuid",
        },
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


class Store(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: StoreUUID
    name: StoreName
    url: HTTPURLField


class UpdateStore(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: StoreName | None = None
    url: HTTPURLField | None = None
