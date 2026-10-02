from collections.abc import Callable
from dataclasses import dataclass, field

from fastapi import Query

from src.core.sorting import SortSpec, describe_sort, parse_sort
from src.settings import load_settings

_settings = load_settings()


@dataclass
class PaginationParams:
    after: str | None = None
    before: str | None = None
    limit: int = _settings.pagination.default_limit
    sort: SortSpec = field(default_factory=SortSpec)


def pagination_with_sort(allowed: tuple[str, ...], dynamic: tuple[str, ...] = ()) -> Callable[..., PaginationParams]:
    """Build the pagination dependency for a list endpoint.

    `allowed` are the top-level fields it can be sorted by; `dynamic` the store-defined key kinds
    (`attr`, `price`, `region`, `loc`) it additionally accepts, see `src.core.sorting.DYNAMIC_KINDS`.
    """
    description = (
        "Comma-separated sort fields, up to 3; a `-` prefix sorts descending (`-created_at,name`). "
        f"Allowed: {describe_sort(allowed, dynamic)}. Defaults to creation order. A cursor is only valid with the "
        "`sort` it was issued for."
    )
    if dynamic:
        description += (
            " `attr:`/`price:`/`region:`/`loc:` keys sort by a store-defined value (e.g. `-price:retail`, "
            "`attr:weight`, `region:US:retail`); documents without it count as lowest, so come first ascending "
            "and last descending. Such sorts are not index-backed, and a key should hold a single value type."
        )

    def dependency(
        after: str | None = Query(None, description="Cursor for forward pagination"),
        before: str | None = Query(None, description="Cursor for backward pagination"),
        limit: int = Query(_settings.pagination.default_limit, ge=1, le=_settings.pagination.max_limit),
        sort: str | None = Query(None, description=description),
    ) -> PaginationParams:
        return PaginationParams(after=after, before=before, limit=limit, sort=parse_sort(sort, allowed, dynamic))

    return dependency
