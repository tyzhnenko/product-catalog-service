from typing import Annotated

from pydantic import UUID7, BaseModel, ConfigDict, Field

from src.domain.types.attributes import AttributesMap
from src.domain.types.media import Image
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap

VariantUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a variant",
        json_schema_extra={
            "format": "uuid",
        },
    ),
]


VariantTitle = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Title of the variant",
    ),
]


VariantSKU = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Stock Keeping Unit of the variant",
    ),
]

VariantUPC = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Universal Product Code of the variant",
    ),
]


VariantEAN = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="European Article Number of the variant",
    ),
]


VariantJAN = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Japanese Article Number of the variant",
    ),
]


VariantISBN = Annotated[
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


VariantOptions = Annotated[
    list[VariantOption],
    Field(
        default_factory=list,
        description="Additional options for the variant as key-value pairs",
    ),
]

VariantImages = Annotated[
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


class ProductVariant(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        title="ProductVariant",
        json_schema_extra={
            "description": "Product variant information",
        },
    )

    id: VariantUUID
    product_id: UUID7
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
