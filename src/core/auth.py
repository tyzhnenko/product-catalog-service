from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.core.logging import logger
from src.settings import Settings, load_settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)


def rw_access(
    api_key_value: Annotated[str, Security(api_key_header)],
    settings: Annotated[Settings, Depends(load_settings)],
):
    if api_key_value != settings.auth.rw_x_api_key:
        logger.warning("Unauthorized access attempt with invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


def ro_access(
    api_key_value: Annotated[str, Security(api_key_header)],
    settings: Annotated[Settings, Depends(load_settings)],
):
    if api_key_value not in {settings.auth.rw_x_api_key, settings.auth.ro_x_api_key}:
        logger.warning("Unauthorized access attempt with invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
