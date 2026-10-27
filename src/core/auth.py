import secrets
from collections.abc import Iterable
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.core.logging import logger
from src.settings import Settings, get_settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)


def _matches_any(presented: str, configured: Iterable[str | None]) -> bool:
    # Bytes: compare_digest raises TypeError on non-ASCII str. No short-circuit: every key is always compared.
    presented_bytes = presented.encode()
    results = [
        secrets.compare_digest(presented_bytes, key.encode()) for key in configured if key is not None and key != ""
    ]
    return any(results)


def rw_access(
    api_key_value: Annotated[str, Security(api_key_header)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    if not _matches_any(api_key_value, [settings.auth.rw_x_api_key]):
        logger.warning("Unauthorized access attempt with invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


def ro_access(
    api_key_value: Annotated[str, Security(api_key_header)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    if not _matches_any(api_key_value, [settings.auth.rw_x_api_key, settings.auth.ro_x_api_key]):
        logger.warning("Unauthorized access attempt with invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
