from typing import Annotated

from pydantic import HttpUrl

URLField = Annotated[str, HttpUrl]
