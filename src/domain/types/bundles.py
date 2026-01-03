from typing import Annotated

from pydantic import UUID7, BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime

from src.domain.types.attributes import AttributesMap
from src.domain.types.categories import CategoryUUID
from src.domain.types.prices import LocationPriceMap, PriceMap, RegionPriceMap
from src.domain.types.variants import VariantUUID

BundleUUID = Annotated[
    UUID7,
    Field(
        ...,
        description="Unique identifier for a bundle",
        json_schema_extra={
            "format": "uuid",
        },
    ),
]

BundleName = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="Name of the bundle",
    ),
]

BundleDescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Description of the bundle",
    ),
]

BundleComponent = Annotated[
    VariantUUID,
    Field(
        ...,
        description="Identifier of a variant included in the bundle",
    ),
]

BundleComponents = Annotated[
    list[BundleComponent],
    Field(
        default_factory=list,
        description="List of variant identifiers included in the bundle",
    ),
]

BundleCategory = Annotated[
    CategoryUUID,
    Field(
        ...,
        description="Category identifier for the bundle",
    ),
]

BundleCategories = Annotated[
    list[BundleCategory],
    Field(
        default_factory=list,
        description="List of category identifiers for the bundle",
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


class Bundle(BaseModel):
    id: BundleUUID
    name: BundleName
    description: BundleDescription | None = None
    components: BundleComponents | None = None
    attributes: AttributesMap | None = None
    categories: BundleCategories | None = None
    price: PriceMap | None = None
    location_price: LocationPriceMap | None = None
    region_price: RegionPriceMap | None = None
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
