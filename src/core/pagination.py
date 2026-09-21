from dataclasses import dataclass

from fastapi import Query

from src.settings import load_settings

_settings = load_settings()


@dataclass
class PaginationParams:
    after: str | None = Query(None, description="Cursor for forward pagination")
    before: str | None = Query(None, description="Cursor for backward pagination")
    limit: int = Query(_settings.pagination.default_limit, ge=1, le=_settings.pagination.max_limit)
