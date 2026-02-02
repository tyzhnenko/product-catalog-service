from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field

from src.domain.types.attributes import AttributesMap
from src.domain.types.stores import StoreID

type LocationID = Annotated[
    PydanticObjectId,
    Field(
        ...,
        description="Unique identifier for a location",
    ),
]

type LocationName = Annotated[
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

    id: LocationID
    name: LocationName
    store_id: StoreID
    attributes: AttributesMap


class UpdateLocation(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: LocationName | None = None
    attributes: AttributesMap | None = None
