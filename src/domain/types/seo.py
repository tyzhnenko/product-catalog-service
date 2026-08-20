from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

type SEOSlug = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=64,
        description="Slug",
    ),
]

type SEOTitle = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=128,
        description="SEO title",
    ),
]

type SEODescription = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=1024,
        description="SEO description",
    ),
]

type SEOKeywords = Annotated[
    str,
    Field(
        ...,
        min_length=1,
        max_length=256,
        description="SEO keywords",
    ),
]


class SEO(BaseModel):
    """SEO information."""

    model_config = ConfigDict(
        title="SEO",
        json_schema_extra={
            "description": "SEO information",
        },
    )

    slug: SEOSlug | None = None
    title: SEOTitle | None = None
    description: SEODescription | None = None
    keywords: SEOKeywords | None = None
