import asyncio
import base64
import os
from decimal import Decimal, InvalidOperation
from itertools import accumulate
from pathlib import Path
from typing import Any, Callable, NoReturn, TypeVar, overload

from beanie import Document, PydanticObjectId
from beanie.odm.queries.find import FindMany
from bson.errors import InvalidId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

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


def parse_ref(ref: str, slug_field: str = "seo.slug") -> dict[str, Any]:
    """Resolve a path-param ref to a Mongo filter clause.

    A value prefixed with 's-' is treated as a slug lookup on `slug_field`; anything else is
    parsed as an ObjectId. A 24-hex-char ObjectId can never start with 's-', so the two forms
    are unambiguous.
    """
    if ref.startswith("s-"):
        return {slug_field: ref[2:]}
    try:
        return {"_id": PydanticObjectId(ref)}
    except InvalidId:
        raise ValueError(f"Invalid reference: {ref}") from None


def raise_for_duplicate_key(exc: DuplicateKeyError) -> NoReturn:
    key_pattern = (exc.details or {}).get("keyPattern", {})
    fields = ", ".join(key_pattern.keys()) or "unknown field"
    raise HTTPException(status_code=409, detail=f"Duplicate value for: {fields}") from exc


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
    count_query = query.document_model.find(query.get_filter_query())

    if after is not None:
        cursor_id = decode_cursor(after)
        docs_coro = query.find({"_id": {"$gt": cursor_id}}).sort("+_id").limit(limit + 1).to_list()
        total, docs = await asyncio.gather(count_query.count(), docs_coro)
        has_next = len(docs) > limit
        has_prev = True
        if has_next:
            docs = docs[:limit]
    elif before is not None:
        cursor_id = decode_cursor(before)
        docs_coro = query.find({"_id": {"$lt": cursor_id}}).sort("-_id").limit(limit + 1).to_list()
        total, docs = await asyncio.gather(count_query.count(), docs_coro)
        has_prev = len(docs) > limit
        has_next = True
        if has_prev:
            docs = docs[:limit]
        docs.reverse()
    else:
        docs_coro = query.sort("+_id").limit(limit + 1).to_list()
        total, docs = await asyncio.gather(count_query.count(), docs_coro)
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
        total=total,
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


_PRICE_OPS = (">=", "<=")


def _split_price_op(token: str) -> tuple[str, str | None, Decimal | None]:
    """Split a '<key><op><value>' token into (key, op, value), or (token, None, None) if no op is present."""
    for op in _PRICE_OPS:
        if op in token:
            key, _, raw_value = token.partition(op)
            try:
                return key, op, Decimal(raw_value)
            except InvalidOperation as ex:
                raise HTTPException(status_code=400, detail=f"Invalid price value in '{token}'") from ex
    return token, None, None


def build_price_search_filter(tokens: list[str]) -> dict:
    """Build a MongoDB filter dict from a list of price search tokens.

    Tokens:
    - '<key>>=<value>' / '<key><=<value>': top-level price.<key>.value range.
    - 'loc:<id>': variant priced at that location (any key).
    - 'loc:<id>:<key>': that key present for the location.
    - 'loc:<id>:<key>>=<value>' / '<=': ranged location price.
    - 'region:<code>[:<key>[<op><value>]]': same as 'loc:', scoped to region_price.

    A bare key with no operator is a no-op. >= and <= tokens targeting the same path merge
    into one $gte/$lte condition.
    """
    existence: dict[str, dict] = {}
    conditions: dict[str, dict] = {}

    for token in tokens:
        scope, sep, rest = token.partition(":")
        if sep and scope in ("loc", "region"):
            prefix = "location_price" if scope == "loc" else "region_price"
            scope_id, _, remainder = rest.partition(":")
            if not scope_id:
                continue
            if not remainder:
                existence[f"{prefix}.{scope_id}"] = {"$exists": True, "$ne": {}}
                continue
            key, op, value = _split_price_op(remainder)
            if op is None:
                existence[f"{prefix}.{scope_id}.{key}"] = {"$exists": True}
                continue
            path = f"{prefix}.{scope_id}.{key}.value"
        else:
            key, op, value = _split_price_op(token)
            if op is None:
                continue
            path = f"price.{key}.value"

        conditions.setdefault(path, {})["$gte" if op == ">=" else "$lte"] = value

    return {**existence, **conditions}
