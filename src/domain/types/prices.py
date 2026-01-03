from decimal import Decimal
from typing import Annotated, Literal

import bson
import pydantic
from pydantic import BaseModel, Field

from src.domain.types.common import CountryCode
from src.domain.types.locations import LocationUUID

PriceName = Annotated[
    str,
    Field(
        ...,
        description="Name of the attribute",
    ),
]

DecimalPriceValue = Annotated[
    Decimal,
    Field(
        ...,
        description="Price represented as a decimal in string format",
    ),
    pydantic.BeforeValidator(lambda v: v.to_decimal() if isinstance(v, bson.Decimal128) else v),
]


class DecimalPrice(BaseModel):
    type: Literal["decimal"] = "decimal"
    name: PriceName
    value: DecimalPriceValue


class DecimalRangePrice(BaseModel):
    type: Literal["decimal_range"] = "decimal_range"
    name: PriceName
    min_value: DecimalPriceValue
    max_value: DecimalPriceValue


class DecimalQuantityPrice(BaseModel):
    type: Literal["decimal_quantity"] = "decimal_quantity"
    name: PriceName
    min_quantity: int
    value: DecimalPriceValue


Price = Annotated[
    DecimalPrice | DecimalRangePrice | DecimalQuantityPrice,
    Field(
        ...,
        description="Price information which can be of various types",
    ),
]

PriceMap = Annotated[
    dict[str, Price],
    Field(
        default_factory=dict,
        description="Mapping of price identifiers to their corresponding Price objects",
    ),
]

LocationPriceMap = Annotated[
    dict[LocationUUID, PriceMap],
    Field(
        default_factory=dict,
        description="Mapping of location identifiers to their corresponding PriceMap",
    ),
]

RegionPriceMap = Annotated[
    dict[CountryCode, PriceMap],
    Field(
        default_factory=dict,
        description="Mapping of region identifiers to their corresponding PriceMap",
    ),
]
