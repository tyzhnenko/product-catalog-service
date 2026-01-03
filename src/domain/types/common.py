from typing import Annotated

from pydantic import Field
from pydantic_extra_types.country import CountryAlpha2

CountryCode = Annotated[
    CountryAlpha2,
    Field(
        ...,
        description="ISO 3166-1 alpha-2 country code",
    ),
]
