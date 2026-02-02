from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime

from src.domain.types.attributes import AttributesMap
from src.domain.types.categories import CategoryID
from src.domain.types.media import Image
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap
from src.domain.types.variants import VariantID

type BundleID = Annotated[
    PydanticObjectId,
    Field(
        ...,
        description="Unique identifier for a bundle",
    ),
]

type BundleName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Name of the bundle",
    ),
]

type BundleDescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Description of the bundle",
    ),
]

type BundleComponent = Annotated[
    VariantID,
    Field(
        ...,
        description="Identifier of a variant included in the bundle",
    ),
]

type BundleComponents = Annotated[
    list[BundleComponent],
    Field(
        default_factory=list,
        description="List of variant identifiers included in the bundle",
    ),
]

type BundleCategory = Annotated[
    CategoryID,
    Field(
        ...,
        description="Category identifier for the bundle",
    ),
]

type BundleCategories = Annotated[
    list[BundleCategory],
    Field(
        default_factory=list,
        description="List of category identifiers for the bundle",
    ),
]

type BundleImages = Annotated[
    list[Image],
    Field(
        default_factory=list,
        description="List of images associated with the bundle",
    ),
]


class NewBundle(BaseModel):
    name: BundleName
    description: BundleDescription | None = None
    components: BundleComponents | None = None
    attributes: AttributesMap | None = None
    categories: BundleCategories | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: BundleImages | None = None


class Bundle(BaseModel):
    id: BundleID
    name: BundleName
    description: BundleDescription | None = None
    components: BundleComponents | None = None
    attributes: AttributesMap | None = None
    categories: BundleCategories | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: BundleImages | None = None
    updated_at: DateTime
    created_at: DateTime


class UpdateBundle(BaseModel):
    name: BundleName | None = None
    description: BundleDescription | None = None
    components: BundleComponents | None = None
    attributes: AttributesMap | None = None
    categories: BundleCategories | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
    images: BundleImages | None = None
