from enum import Enum
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.pendulum_dt import DateTime

from src.core.utils import split_path
from src.domain.types.attributes import AttributesMap
from src.domain.types.media import Image
from src.domain.types.refs import ObjectIdRef, SlugRef
from src.domain.types.seo import SEO

type CategoryID = Annotated[
    PydanticObjectId,
    Field(
        ...,
        title="Category ID",
        description="Unique identifier for a category",
    ),
]

type CategoryRef = Annotated[
    ObjectIdRef | SlugRef,
    Field(
        title="Category Ref",
        description="Category ID or slug ref (prefixed 's-')",
    ),
]

type CategoryName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Name of the category",
    ),
]

type CategoryDescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Description of the category",
    ),
]

type CategoryPath = Annotated[
    str,
    Field(
        ...,
        description=(
            "Path of the category. Example: '/electronics/laptops'. Root categories have path as '/electronics'."
        ),
        pattern=r"^(/[\w.-]+)+/?$",
    ),
]

type CategoryImages = Annotated[
    list[Image],
    Field(
        default_factory=list,
        description="List of images associated with the category",
    ),
]


class CategoryStatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


type CategoryStatus = Annotated[
    CategoryStatusEnum,
    Field(
        ...,
        description="Status of the category",
    ),
]


class NewCategory(BaseModel):
    """Data required to create a new category."""

    model_config = ConfigDict(
        title="NewCategory",
        json_schema_extra={
            "description": "Data required to create a new category",
        },
    )

    name: CategoryName
    description: CategoryDescription | None = None
    status: CategoryStatus = CategoryStatusEnum.ACTIVE
    path: CategoryPath
    seo: SEO | None = None
    attributes: AttributesMap | None = None
    images: CategoryImages | None = None

    @property
    def paths(self) -> list[str]:
        return split_path(self.path)


class Category(BaseModel):
    """Category model."""

    model_config = ConfigDict(
        title="Category",
        from_attributes=True,
        json_schema_extra={
            "description": "Category model",
        },
    )

    id: CategoryID
    name: CategoryName
    description: CategoryDescription | None
    status: CategoryStatus
    path: CategoryPath
    seo: SEO | None
    attributes: AttributesMap | None
    images: CategoryImages | None
    updated_at: DateTime
    created_at: DateTime


class UpdateCategory(BaseModel):
    """Data required to update a category."""

    model_config = ConfigDict(
        title="UpdateCategory",
        json_schema_extra={
            "description": "Data required to update a category",
        },
    )

    name: CategoryName | None = None
    description: CategoryDescription | None = None
    status: CategoryStatus | None = None
    seo: SEO | None = None
    path: CategoryPath | None = None
    attributes: AttributesMap | None = None
    images: CategoryImages | None = None
