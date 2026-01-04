from enum import Enum
from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field
from pydantic_extra_types.pendulum_dt import DateTime

from src.core.utils import split_path
from src.domain.types.attributes import AttributesMap
from src.domain.types.media import Image

CategoryUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a category",
        json_schema_extra={
            "format": "uuid",
        },
    ),
]

CategoryName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Name of the category",
    ),
]

CategoryDescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Description of the category",
    ),
]

CategorySEOSlug = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Slug of the category",
    ),
]

CategorySEOTitle = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=128,
        description="SEO title of the category",
    ),
]

CategorySEODescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=1024,
        description="SEO description of the category",
    ),
]

CategorySEOKeywords = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="SEO keywords of the category",
    ),
]

CategoryPath = Annotated[
    str,
    Field(
        ...,
        description=(
            "Path of the category. Example: '/electronics/laptops'. Root categories have path as '/electronics'."
        ),
        pattern=r"^(/[\w.-]+)+/?$",
    ),
]

CategoryImages = Annotated[
    list[Image],
    Field(
        default_factory=list,
        description="List of images associated with the category",
    ),
]


class CategoryStatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


CategoryStatus = Annotated[
    CategoryStatusEnum,
    Field(
        ...,
        description="Status of the category",
    ),
]


class CategorySEO(BaseModel):
    """SEO information for a category."""

    model_config = ConfigDict(
        title="CategorySEO",
        json_schema_extra={
            "description": "SEO information for a category",
        },
    )

    slug: CategorySEOSlug
    title: CategorySEOTitle
    description: CategorySEODescription
    keywords: CategorySEOKeywords
    path: CategoryPath


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
    seo: CategorySEO | None = None
    attributes: AttributesMap | None = None
    images: CategoryImages | None = None

    @property
    def paths(self) -> list[str]:
        return split_path(self.path)


class Category(BaseModel):
    """Category model."""

    model_config = ConfigDict(
        title="Category",
        json_schema_extra={
            "description": "Category model",
        },
    )

    id: CategoryUUID
    name: CategoryName
    description: CategoryDescription | None
    status: CategoryStatus
    path: CategoryPath
    seo: CategorySEO | None
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
    seo: CategorySEO | None = None
    path: CategoryPath | None = None
    attributes: AttributesMap | None = None
    images: CategoryImages | None = None
