from enum import Enum
from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field
from pydantic_extra_types.pendulum_dt import DateTime

from src.domain.categories import CategoryUUID
from src.domain.types.attributes import AttributesMap

type ProductUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a product",
        json_schema_extra={
            "format": "uuid",
        },
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


type ProductSEOSlug = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Slug of the product",
    ),
]

type ProductCategory = Annotated[
    CategoryUUID,
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

type ProductSEOTitle = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=128,
        description="SEO title of the product",
    ),
]

type ProductSEODescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=1024,
        description="SEO description of the product",
    ),
]

type ProductSEOKeywords = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="SEO keywords of the product",
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


class ProductSEO(BaseModel):
    """SEO information for a product."""

    model_config = ConfigDict(
        title="ProductSEO",
        json_schema_extra={
            "description": "SEO information for a product",
        },
    )

    slug: ProductSEOSlug | None = None
    title: ProductSEOTitle | None = None
    description: ProductSEODescription | None = None
    keywords: ProductSEOKeywords | None = None


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
    seo: ProductSEO | None = None
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

    id: ProductUUID
    name: ProductName
    description: ProductDescription | None = None
    brand: ProductBrand | None = None
    tags: ProductTags
    seo: ProductSEO | None = None
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
    seo: ProductSEO | None = None
    status: ProductStatus | None = None
    categories: ProductCategories | None = None
    attributes: AttributesMap | None = None
