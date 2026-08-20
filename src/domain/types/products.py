from enum import Enum
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.pendulum_dt import DateTime

from src.domain.types.attributes import AttributesMap
from src.domain.types.categories import CategoryID
from src.domain.types.refs import ObjectIdRef, SlugRef
from src.domain.types.seo import SEO

type ProductID = Annotated[
    PydanticObjectId,
    Field(
        ...,
        title="Product ID",
        description="Unique identifier for a product",
    ),
]

type ProductRef = Annotated[
    ObjectIdRef | SlugRef,
    Field(
        title="Product Ref",
        description="Product ID or slug ref (prefixed 's-')",
    ),
]

type ProductName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=512,
        description="Name of the product",
    ),
]

type ProductDescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Description of the product",
    ),
]

type ProductBrand = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=128,
        description="Brand of the product",
    ),
]

type ProductTags = Annotated[
    list[str],
    Field(
        default_factory=list,
        description="Tags associated with the product",
    ),
]


type ProductCategory = Annotated[
    CategoryID,
    Field(
        ...,
        description="Category identifier for the product",
    ),
]

type ProductCategories = Annotated[
    list[ProductCategory],
    Field(
        default_factory=list,
        description="List of category identifiers for the product",
    ),
]


class ProductStatusEnum(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"


type ProductStatus = Annotated[
    ProductStatusEnum,
    Field(
        ProductStatusEnum.ACTIVE,
        description="Status of the product",
    ),
]


class NewProduct(BaseModel):
    model_config = ConfigDict(
        title="NewProduct",
        json_schema_extra={
            "description": "Data required to create a new product",
        },
    )

    name: ProductName
    description: ProductDescription | None = None
    brand: ProductBrand | None = None
    tags: ProductTags
    seo: SEO | None = None
    categories: ProductCategories | None = None
    attributes: AttributesMap | None = None


class Product(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        title="Product",
        json_schema_extra={
            "description": "Product information",
        },
    )

    id: ProductID
    name: ProductName
    description: ProductDescription | None = None
    brand: ProductBrand | None = None
    tags: ProductTags
    seo: SEO | None = None
    status: ProductStatus
    categories: ProductCategories
    attributes: AttributesMap
    updated_at: DateTime
    created_at: DateTime


class UpdateProduct(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        title="UpdateProduct",
        json_schema_extra={
            "description": "Data required to update a product",
        },
    )

    name: ProductName | None = None
    description: ProductDescription | None = None
    brand: ProductBrand | None = None
    tags: ProductTags | None = None
    seo: SEO | None = None
    status: ProductStatus | None = None
    categories: ProductCategories | None = None
    attributes: AttributesMap | None = None
