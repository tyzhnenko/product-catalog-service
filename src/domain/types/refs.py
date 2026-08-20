from typing import Annotated

from pydantic import Field

type ObjectIdRef = Annotated[
    str,
    Field(
        pattern=r"^[0-9a-fA-F]{24}$",
        description="24-character hex ObjectId",
    ),
]

type SlugRef = Annotated[
    str,
    Field(
        pattern=r"^s-.{1,512}$",
        description="Slug ref, prefixed with 's-'",
    ),
]
