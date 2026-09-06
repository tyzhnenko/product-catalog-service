"""Base model for all application models."""

from datetime import datetime, timezone

from beanie import Document, Save, before_event
from pydantic import Field


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class BaseAppDocument(Document):
    """Base model for all application models."""

    updated_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)
    deleted_at: datetime | None = None

    @before_event(Save)
    def bump_updated_at(self) -> None:
        self.updated_at = utc_now()
