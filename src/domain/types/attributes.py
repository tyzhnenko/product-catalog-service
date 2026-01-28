from decimal import Decimal
from typing import Annotated, Literal, Text
from uuid import UUID

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


type Attribute = Annotated[
    StringAttribute
    | TextAttribute
    | IntegerAttribute
    | BoolAttribute
    | FloatAttribute
    | DateAttribute
    | DateTimeAttribute
    | UUIDAttribute
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
    | ListOfURLsAttribute,
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
