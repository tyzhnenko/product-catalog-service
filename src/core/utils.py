import base64
import os
from decimal import Decimal
from itertools import accumulate
from pathlib import Path
from typing import Any, Callable, TypeVar, overload

from beanie import Document, PydanticObjectId
from beanie.odm.queries.find import FindMany
from fastapi import HTTPException

from src.core.types import PaginatedResponse

DocT = TypeVar("DocT", bound=Document)
T = TypeVar("T")


def split_path(path: str) -> list[str]:
    """Return cumulative hierarchical paths for the given path.

    The input string is converted to a :class:`pathlib.Path`, and its
    components are combined left-to-right to produce a list of
    progressively longer paths.

    For example:

    - For a path: ``"/electronics/laptops"`` ->
      ``["/", "/electronics", "/electronics/laptops"]``.

    Args:
        path (str): The input path string.

    Returns:
        list[str]: A list of cumulative paths as strings.

    """
    _path = Path(path)
    return list(
        accumulate(
            _path.parts,
            lambda x, y: os.path.join(x, y),
        )
    )


def encode_cursor(object_id: PydanticObjectId) -> str:
    return base64.urlsafe_b64encode(str(object_id).encode()).decode()


def decode_cursor(cursor: str) -> PydanticObjectId:
    try:
        decoded = base64.urlsafe_b64decode(cursor.encode()).decode()
        return PydanticObjectId(decoded)
    except Exception as ex:
        raise HTTPException(status_code=400, detail="Invalid cursor") from ex


@overload
async def paginate(
    query: FindMany[DocT],
    after: str | None,
    before: str | None,
    limit: int,
    transform: Callable[[DocT], T],
) -> PaginatedResponse[T]: ...


@overload
async def paginate(
    query: FindMany[DocT],
    after: str | None,
    before: str | None,
    limit: int,
    transform: None = None,
) -> PaginatedResponse[DocT]: ...


async def paginate(
    query: FindMany[DocT],
    after: str | None,
    before: str | None,
    limit: int,
    transform: Callable[[DocT], T] | None = None,
) -> PaginatedResponse[Any]:
    if after is not None:
        cursor_id = decode_cursor(after)
        docs = await query.find({"_id": {"$gt": cursor_id}}).sort("+_id").limit(limit + 1).to_list()
        has_next = len(docs) > limit
        has_prev = True
        if has_next:
            docs = docs[:limit]
    elif before is not None:
        cursor_id = decode_cursor(before)
        docs = await query.find({"_id": {"$lt": cursor_id}}).sort("-_id").limit(limit + 1).to_list()
        has_prev = len(docs) > limit
        has_next = True
        if has_prev:
            docs = docs[:limit]
        docs.reverse()
    else:
        docs = await query.sort("+_id").limit(limit + 1).to_list()
        has_next = len(docs) > limit
        has_prev = False
        if has_next:
            docs = docs[:limit]

    items: list[Any] = [transform(doc) for doc in docs] if transform is not None else docs

    start_cursor = None
    end_cursor = None
    if docs and docs[0].id is not None:
        start_cursor = encode_cursor(docs[0].id)
    if docs and docs[-1].id is not None:
        end_cursor = encode_cursor(docs[-1].id)

    return PaginatedResponse(
        items=items,
        start_cursor=start_cursor,
        end_cursor=end_cursor,
        has_next=has_next,
        has_prev=has_prev,
    )


def _coerce_attr_value(raw: str) -> bool | int | float | str:
    lower = raw.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def build_attribute_filter(attrs: list[str]) -> dict:
    """Build a MongoDB filter dict from a list of 'key:value' attribute filter strings.

    Same key with multiple values → OR via $in.
    Different keys → AND (implicit MongoDB dict merge).
    Entries without a colon are silently ignored.
    """
    grouped: dict[str, list] = {}
    for entry in attrs:
        if ":" not in entry:
            continue
        key, _, raw_value = entry.partition(":")
        grouped.setdefault(key, []).append(_coerce_attr_value(raw_value))

    result: dict = {}
    for key, values in grouped.items():
        mongo_key = f"attributes.{key}.value"
        result[mongo_key] = values[0] if len(values) == 1 else {"$in": values}
    return result


def build_price_filter(
    price_key: str | None,
    price_min: Decimal | None,
    price_max: Decimal | None,
) -> dict:
    """Build a MongoDB filter dict for the top-level price map."""
    if not price_key:
        return {}
    conditions: dict = {}
    if price_min is not None:
        conditions["$gte"] = price_min
    if price_max is not None:
        conditions["$lte"] = price_max
    if not conditions:
        return {}
    return {f"price.{price_key}.value": conditions}


def build_location_price_filter(
    location_price_id: str | None,
    location_price_key: str | None,
    location_price_min: Decimal | None,
    location_price_max: Decimal | None,
) -> dict:
    """Build a MongoDB filter dict for the location_price map."""
    if not location_price_id or not location_price_key:
        return {}
    conditions: dict = {}
    if location_price_min is not None:
        conditions["$gte"] = location_price_min
    if location_price_max is not None:
        conditions["$lte"] = location_price_max
    if not conditions:
        return {}
    return {f"location_price.{location_price_id}.{location_price_key}.value": conditions}


def build_region_price_filter(
    region_price_code: str | None,
    region_price_key: str | None,
    region_price_min: Decimal | None,
    region_price_max: Decimal | None,
) -> dict:
    """Build a MongoDB filter dict for the region_price map."""
    if not region_price_code or not region_price_key:
        return {}
    conditions: dict = {}
    if region_price_min is not None:
        conditions["$gte"] = region_price_min
    if region_price_max is not None:
        conditions["$lte"] = region_price_max
    if not conditions:
        return {}
    return {f"region_price.{region_price_code}.{region_price_key}.value": conditions}
