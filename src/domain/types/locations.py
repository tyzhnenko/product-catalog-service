from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field

from src.domain.types.attributes import AttributesMap
from src.domain.types.stores import StoreUUID

LocationUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a location",
        json_schema_extra={
            "format": "uuid",
        },
    ),
]

LocationName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Name of the location",
    ),
]


class NewLocation(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: LocationName
    attributes: AttributesMap = Field(default_factory=dict)


class Location(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: LocationUUID
    name: LocationName
    store_id: StoreUUID
    attributes: AttributesMap


class UpdateLocation(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: LocationName | None = None
    attributes: AttributesMap | None = None
