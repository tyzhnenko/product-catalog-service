from typing import Annotated

from pydantic import BaseModel, Field

from src.domain.types.attributes import AttributesMap
from src.domain.types.base import HTTPURLField

type ImageURL = Annotated[
    HTTPURLField,
    Field(
        ...,
        description="URL of the image",
    ),
]

type ImageHeight = Annotated[
    int,
    Field(
        ...,
        gt=0,
        description="Height of the image in pixels",
    ),
]

type ImageWidth = Annotated[
    int,
    Field(
        ...,
        gt=0,
        description="Width of the image in pixels",
    ),
]

type ImageAltText = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=512,
        description="Alternative text for the image",
    ),
]


class Image(BaseModel):
    url: ImageURL
    alt_text: ImageAltText | None = None
    height: ImageHeight | None = None
    width: ImageWidth | None = None
    attributes: AttributesMap | None = None
