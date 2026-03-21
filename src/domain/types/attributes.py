from decimal import Decimal
from typing import Annotated, Literal, Text
from uuid import UUID

import bson
import pydantic
from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import Date, DateTime

from src.domain.types.base import HTTPURLField

type StringAttributeValue = Annotated[
    str,
    Field(
        ...,
        description="String value",
    ),
]


type TextAttributeValue = Annotated[
    Text,
    Field(
        ...,
        description="Text value",
    ),
]


type IntegerAttributeValue = Annotated[
    int,
    Field(
        ...,
        description="Integer value",
    ),
]


type FloatAttributeValue = Annotated[
    float,
    Field(
        ...,
        description="Floating point number value",
    ),
]


type DecimalAttributeValue = Annotated[
    Decimal,
    Field(
        ...,
        description="Decimal value represented as a float in string format",
    ),
    pydantic.BeforeValidator(lambda v: v.to_decimal() if isinstance(v, bson.Decimal128) else v),
]


type AttributeName = Annotated[
    str,
    Field(
        ...,
        description="Name of the attribute",
    ),
]

type DateAttributeValue = Annotated[
    Date,
    Field(
        ...,
        description="Date value in ISO 8601 format",
        json_schema_extra={"format": "date"},
    ),
]


type DateTimeAttributeValue = Annotated[
    DateTime,
    Field(
        ...,
        description="Datetime value in ISO 8601 format",
        json_schema_extra={"format": "date-time"},
    ),
]


type UUIDAttributeValue = Annotated[
    UUID,
    Field(
        ...,
        description="UUID value",
        json_schema_extra={"format": "uuid"},
    ),
]

type ObjectIdValue = Annotated[PydanticObjectId, Field(..., description="ObjectId value")]


type URLAttributeValue = Annotated[
    HTTPURLField,
    Field(
        ...,
        description="URL value",
        json_schema_extra={"format": "uri"},
    ),
]


class StringAttribute(BaseModel):
    type: Literal["string"] = "string"
    name: AttributeName
    value: StringAttributeValue


class TextAttribute(BaseModel):
    type: Literal["text"] = "text"
    name: AttributeName
    value: TextAttributeValue


class IntegerAttribute(BaseModel):
    type: Literal["integer"] = "integer"
    name: AttributeName
    value: IntegerAttributeValue


class FloatAttribute(BaseModel):
    type: Literal["float"] = "float"
    name: AttributeName
    value: FloatAttributeValue


class DecimalAttribute(BaseModel):
    type: Literal["decimal"] = "decimal"
    name: AttributeName
    value: DecimalAttributeValue


class BoolAttribute(BaseModel):
    type: Literal["bool"] = "bool"
    name: AttributeName
    value: Annotated[
        bool,
        Field(
            ...,
            description="Boolean value",
        ),
    ]


class DateAttribute(BaseModel):
    type: Literal["date"] = "date"
    name: AttributeName
    value: DateAttributeValue


class DateTimeAttribute(BaseModel):
    type: Literal["datetime"] = "datetime"
    name: AttributeName
    value: DateTimeAttributeValue


class UUIDAttribute(BaseModel):
    type: Literal["uuid"] = "uuid"
    name: AttributeName
    value: UUIDAttributeValue


class ObjectIdAttribute(BaseModel):
    type: Literal["object_id"] = "object_id"
    name: AttributeName
    value: ObjectIdValue


class URLAttribute(BaseModel):
    type: Literal["url"] = "url"
    name: AttributeName
    value: URLAttributeValue


class FloatRangeAttribute(BaseModel):
    type: Literal["float_range"] = "float_range"
    name: AttributeName
    min_value: FloatAttributeValue
    max_value: FloatAttributeValue


class IntegerRangeAttribute(BaseModel):
    type: Literal["integer_range"] = "integer_range"
    name: AttributeName
    min_value: IntegerAttributeValue
    max_value: IntegerAttributeValue


class DecimalRangeAttribute(BaseModel):
    type: Literal["decimal_range"] = "decimal_range"
    name: AttributeName
    min_value: DecimalAttributeValue
    max_value: DecimalAttributeValue


class ListOfStringsAttribute(BaseModel):
    type: Literal["list_of_strings"] = "list_of_strings"
    name: AttributeName
    values: Annotated[
        list[StringAttributeValue],
        Field(
            ...,
            description="List of string values",
        ),
    ]


class ListOfIntegersAttribute(BaseModel):
    type: Literal["list_of_integers"] = "list_of_integers"
    name: AttributeName
    values: Annotated[
        list[IntegerAttributeValue],
        Field(
            ...,
            description="List of integer values",
        ),
    ]


class ListOfFloatsAttribute(BaseModel):
    type: Literal["list_of_floats"] = "list_of_floats"
    name: AttributeName
    values: Annotated[
        list[FloatAttributeValue],
        Field(
            ...,
            description="List of float values",
        ),
    ]


class ListOfDecimalsAttribute(BaseModel):
    type: Literal["list_of_decimals"] = "list_of_decimals"
    name: AttributeName
    values: Annotated[
        list[DecimalAttributeValue],
        Field(
            ...,
            description="List of decimal values",
        ),
    ]


class ListOfUUIDsAttribute(BaseModel):
    type: Literal["list_of_uuids"] = "list_of_uuids"
    name: AttributeName
    values: Annotated[
        list[UUIDAttributeValue],
        Field(
            ...,
            description="List of UUID values",
        ),
    ]


class ListOfObjectIdsAttribute(BaseModel):
    type: Literal["list_of_object_ids"] = "list_of_object_ids"
    name: AttributeName
    values: Annotated[
        list[ObjectIdValue],
        Field(
            ...,
            description="List of ObjectId values",
        ),
    ]


class ListOfURLsAttribute(BaseModel):
    type: Literal["list_of_urls"] = "list_of_urls"
    name: AttributeName
    values: Annotated[
        list[URLAttributeValue],
        Field(
            ...,
            description="List of URL values",
        ),
    ]


class ListOfDatesAttribute(BaseModel):
    type: Literal["list_of_dates"] = "list_of_dates"
    name: AttributeName
    values: Annotated[
        list[DateAttributeValue],
        Field(
            ...,
            description="List of date values",
        ),
    ]


class ListOfDateTimesAttribute(BaseModel):
    type: Literal["list_of_datetimes"] = "list_of_datetimes"
    name: AttributeName
    values: Annotated[
        list[DateTimeAttributeValue],
        Field(
            ...,
            description="List of datetime values",
        ),
    ]


class MapOfStringsAttribute(BaseModel):
    type: Literal["map_of_strings"] = "map_of_strings"
    name: AttributeName
    values: Annotated[
        dict[str, StringAttributeValue],
        Field(
            ...,
            description="Map of string values",
        ),
    ]


class MapOfIntegersAttribute(BaseModel):
    type: Literal["map_of_integers"] = "map_of_integers"
    name: AttributeName
    values: Annotated[
        dict[str, IntegerAttributeValue],
        Field(
            ...,
            description="Map of integer values",
        ),
    ]


class MapOfFloatsAttribute(BaseModel):
    type: Literal["map_of_floats"] = "map_of_floats"
    name: AttributeName
    values: Annotated[
        dict[str, FloatAttributeValue],
        Field(
            ...,
            description="Map of float values",
        ),
    ]


class MapOfDecimalsAttribute(BaseModel):
    type: Literal["map_of_decimals"] = "map_of_decimals"
    name: AttributeName
    values: Annotated[
        dict[str, DecimalAttributeValue],
        Field(
            ...,
            description="Map of decimal values",
        ),
    ]


class MapOfUUIDsAttribute(BaseModel):
    type: Literal["map_of_uuids"] = "map_of_uuids"
    name: AttributeName
    values: Annotated[
        dict[str, UUIDAttributeValue],
        Field(
            ...,
            description="Map of UUID values",
        ),
    ]


class MapOfObjectIdsAttribute(BaseModel):
    type: Literal["map_of_object_ids"] = "map_of_object_ids"
    name: AttributeName
    values: Annotated[
        dict[str, ObjectIdValue],
        Field(
            ...,
            description="Map of ObjectId values",
        ),
    ]


class MapOfURLsAttribute(BaseModel):
    type: Literal["map_of_urls"] = "map_of_urls"
    name: AttributeName
    values: Annotated[
        dict[str, URLAttributeValue],
        Field(
            ...,
            description="Map of URL values",
        ),
    ]


class MapOfDatesAttribute(BaseModel):
    type: Literal["map_of_dates"] = "map_of_dates"
    name: AttributeName
    values: Annotated[
        dict[str, DateAttributeValue],
        Field(
            ...,
            description="Map of date values",
        ),
    ]


class MapOfDateTimesAttribute(BaseModel):
    type: Literal["map_of_datetimes"] = "map_of_datetimes"
    name: AttributeName
    values: Annotated[
        dict[str, DateTimeAttributeValue],
        Field(
            ...,
            description="Map of datetime values",
        ),
    ]


type Attribute = Annotated[
    StringAttribute
    | TextAttribute
    | IntegerAttribute
    | BoolAttribute
    | FloatAttribute
    | DateAttribute
    | DateTimeAttribute
    | UUIDAttribute
    | ObjectIdAttribute
    | DecimalAttribute
    | URLAttribute
    | FloatRangeAttribute
    | IntegerRangeAttribute
    | DecimalRangeAttribute
    | ListOfStringsAttribute
    | ListOfIntegersAttribute
    | ListOfFloatsAttribute
    | ListOfDecimalsAttribute
    | ListOfUUIDsAttribute
    | ListOfObjectIdsAttribute
    | ListOfURLsAttribute
    | ListOfDatesAttribute
    | ListOfDateTimesAttribute
    | MapOfStringsAttribute
    | MapOfIntegersAttribute
    | MapOfFloatsAttribute
    | MapOfDecimalsAttribute
    | MapOfUUIDsAttribute
    | MapOfObjectIdsAttribute
    | MapOfURLsAttribute
    | MapOfDatesAttribute
    | MapOfDateTimesAttribute,
    Field(
        ...,
        title="Attribute",
        description="Attribute which can be of various types",
    ),
]

type AttributesList = Annotated[
    list[Attribute],
    Field(
        default_factory=list,
        title="Attributes List",
        description="List of attributes",
    ),
]

type AttributesMap = Annotated[
    dict[str, Attribute],
    Field(
        default_factory=dict,
        title="Attributes Map",
        description="Map of attribute name to attribute",
    ),
]

# Alias for backwards compatibility with products
Attributes = AttributesList
