from enum import Enum
from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field

ProductUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a product",
        json_schema_extra={
            "format": "uuid",
        },
    ),
]

ProductName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=512,
        description="Name of the product",
    ),
]

ProductDescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Description of the product",
    ),
]

ProductBrand = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=128,
        description="Brand of the product",
    ),
]

ProductTags = Annotated[
    list[str],
    Field(
        default_factory=list,
        description="Tags associated with the product",
    ),
]


ProductSEOSlug = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Slug of the product",
    ),
]

ProductSEOTitle = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=128,
        description="SEO title of the product",
    ),
]

ProductSEODescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=1024,
        description="SEO description of the product",
    ),
]

ProductSEOKeywords = Annotated[
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


ProductStatus = Annotated[
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
