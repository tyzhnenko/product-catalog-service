"""Base model for all application models."""

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class BaseAppDocument(Document):
    """Base model for all application models."""

    updated_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)
    deleted_at: datetime | None = None
