from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field

from src.domain.types.attributes import AttributesMap
from src.domain.types.media import Image
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap
from src.domain.types.products import PartialProduct, Product, ProductID
from src.domain.types.refs import ObjectIdRef, SlugRef
from src.domain.types.seo import SEO

type VariantID = Annotated[
    PydanticObjectId,
    Field(
        ...,
        title="Variant ID",
        description="Unique identifier for a variant",
    ),
]

type VariantRef = Annotated[
    ObjectIdRef | SlugRef,
    Field(
        title="Variant Ref",
        description="Variant ID or slug ref (prefixed 's-')",
    ),
]


type VariantTitle = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Title of the variant",
    ),
]


type VariantSKU = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Stock Keeping Unit of the variant",
    ),
]

type VariantUPC = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Universal Product Code of the variant",
    ),
]


type VariantEAN = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="European Article Number of the variant",
    ),
]


type VariantJAN = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Japanese Article Number of the variant",
    ),
]


type VariantISBN = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="International Standard Book Number of the variant",
    ),
]


class VariantOption(BaseModel):
    name: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=128,
            description="Name of the option",
        ),
    ]
    value: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=256,
            description="Value of the option",
        ),
    ]


type VariantOptions = Annotated[
    list[VariantOption],
    Field(
        default_factory=list,
        description="Additional options for the variant as key-value pairs",
    ),
]

type VariantImages = Annotated[
    list[Image],
    Field(
        default_factory=list,
        description="List of images associated with the variant",
    ),
]


class NewProductVariant(BaseModel):
    model_config = ConfigDict(
        title="NewProductVariant",
        json_schema_extra={
            "description": "Data required to create a new product variant",
        },
    )

    title: VariantTitle
    sku: VariantSKU | None = None
    upc: VariantUPC | None = None
    ean: VariantEAN | None = None
    jan: VariantJAN | None = None
    isbn: VariantISBN | None = None
    options: VariantOptions
    attributes: AttributesMap | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: VariantImages | None = None
    seo: SEO | None = None


class ProductVariant(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        title="ProductVariant",
        json_schema_extra={
            "description": "Product variant information",
        },
    )

    id: VariantID
    product_id: ProductID
    title: VariantTitle
    sku: VariantSKU | None = None
    upc: VariantUPC | None = None
    ean: VariantEAN | None = None
    jan: VariantJAN | None = None
    isbn: VariantISBN | None = None
    options: VariantOptions
    attributes: AttributesMap | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: VariantImages | None = None
    seo: SEO | None = None


class PartialProductVariant(BaseModel):
    """Sparse `ProductVariant` returned when the `fields` query param narrows the response."""

    model_config = ConfigDict(
        from_attributes=True,
        title="PartialProductVariant",
        json_schema_extra={
            "description": "Product variant information, limited to the fields requested via the `fields` query param",
        },
    )

    id: VariantID
    product_id: ProductID | None = None
    title: VariantTitle | None = None
    sku: VariantSKU | None = None
    upc: VariantUPC | None = None
    ean: VariantEAN | None = None
    jan: VariantJAN | None = None
    isbn: VariantISBN | None = None
    options: VariantOptions | None = None
    attributes: AttributesMap | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: VariantImages | None = None
    seo: SEO | None = None


class ProductWithVariants(Product):
    """`Product` with its variants embedded, returned when `include=variants` is requested."""

    model_config = ConfigDict(
        title="ProductWithVariants",
        json_schema_extra={
            "description": "Product information, including its variants (requested via `include=variants`)",
        },
    )

    variants: list[ProductVariant]


class PartialProductWithVariants(PartialProduct):
    """`PartialProduct` with its variants embedded, returned when `include=variants` and `fields` are combined."""

    model_config = ConfigDict(
        title="PartialProductWithVariants",
        json_schema_extra={
            "description": (
                "Product information, including its variants (requested via `include=variants`), "
                "limited to the fields requested via the `fields` query param"
            ),
        },
    )

    variants: list[ProductVariant]


class UpdateProductVariant(BaseModel):
    model_config = ConfigDict(
        title="UpdateProductVariant",
        json_schema_extra={
            "description": "Data required to update a product variant",
        },
    )

    title: VariantTitle | None = None
    sku: VariantSKU | None = None
    upc: VariantUPC | None = None
    ean: VariantEAN | None = None
    jan: VariantJAN | None = None
    isbn: VariantISBN | None = None
    options: VariantOptions | None = None
    attributes: AttributesMap | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: VariantImages | None = None
    seo: SEO | None = None
