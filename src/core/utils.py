import asyncio
import base64
import os
import re
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

    # Parametrize on the items' actual runtime type (all items share one, since `transform` is applied
    # uniformly) rather than returning a bare, unparametrized PaginatedResponse. Handlers whose response_model
    # is a union of PaginatedResponse[X] | PaginatedResponse[PartialX] rely on this: an unparametrized instance
    # isn't an exact match for either union member, so FastAPI falls back to structurally coercing `items` into
    # whichever member validates first — which can silently be the wrong one whenever the fields a partial
    # response omitted happen to be optional on the full model too, defeating `fields` for that response.
    item_type: type[Any] = type(items[0]) if items else object
    return PaginatedResponse[item_type](  # type: ignore[valid-type]
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


_OBJECT_ID_RE = re.compile(r"[0-9a-fA-F]{24}")

# Aggregation-expression building blocks for the unscoped case, where location keys are not known up front.
_PRICED_LOCATIONS = {
    "$filter": {
        "input": {"$objectToArray": {"$ifNull": ["$location_price", {}]}},
        "as": "lp",
        "cond": {"$gt": [{"$size": {"$objectToArray": {"$ifNull": ["$$lp.v", {}]}}}, 0]},
    }
}
_OUT_OF_STOCK_LOCATIONS = {
    "$map": {
        "input": {
            "$filter": {
                "input": {"$objectToArray": {"$ifNull": ["$attributes.locations_availability.values", {}]}},
                "as": "av",
                "cond": {"$eq": ["$$av.v", "out_of_stock"]},
            }
        },
        "as": "out",
        "in": "$$out.k",
    }
}


def _parse_availability(value: str) -> tuple[str | None, bool]:
    """Parse an ``availability`` query value into ``(location_id, want_in_stock)``.

    Accepted: 'in_stock', 'out_of_stock', 'loc:<id>' (same as in stock), 'loc:<id>:in_stock',
    'loc:<id>:out_of_stock'. Anything else raises a 422.
    """
    if value in ("in_stock", "out_of_stock"):
        return None, value == "in_stock"

    scope, _, rest = value.partition(":")
    loc_id, _, state = rest.partition(":")
    if scope != "loc" or state not in ("", "in_stock", "out_of_stock") or not _OBJECT_ID_RE.fullmatch(loc_id):
        raise HTTPException(status_code=422, detail=f"Invalid availability filter: '{value}'")
    return loc_id.lower(), state != "out_of_stock"


def _build_priced_filter(location_id: str | None) -> dict:
    """Variant filter: has a price (an offer) at the location, or at any location when ``location_id`` is None."""
    if location_id is not None:
        return {f"location_price.{location_id}": {"$exists": True, "$ne": {}}}
    return {"$expr": {"$gt": [{"$size": _PRICED_LOCATIONS}, 0]}}


def _build_in_stock_filter(location_id: str | None) -> dict:
    """Variant filter: in stock at the location (or at any priced location when ``location_id`` is None).

    A variant is in stock at a priced location unless ``locations_availability`` explicitly says 'out_of_stock'
    for it. ``$ne`` also matches a missing attribute or a missing key, so nothing needs backfilling, and
    availability entries for locations without a price never count.
    """
    if location_id is not None:
        return {
            **_build_priced_filter(location_id),
            f"attributes.locations_availability.values.{location_id}": {"$ne": "out_of_stock"},
        }
    in_stock_at_loc = {"$not": [{"$in": ["$$loc.k", _OUT_OF_STOCK_LOCATIONS]}]}
    return {"$expr": {"$anyElementTrue": [{"$map": {"input": _PRICED_LOCATIONS, "as": "loc", "in": in_stock_at_loc}}]}}


def build_availability_filter(value: str | None) -> dict:
    """Build a MongoDB variant filter dict from an availability query value.

    Values: 'in_stock', 'out_of_stock', 'loc:<id>' (same as in stock), 'loc:<id>:in_stock',
    'loc:<id>:out_of_stock'. None means no filter; anything else raises a 422.
    Out of stock means the variant has an offer (at the location, or anywhere) but is not in stock there.
    """
    if value is None:
        return {}
    location_id, in_stock = _parse_availability(value)
    if in_stock:
        return _build_in_stock_filter(location_id)
    return {"$and": [_build_priced_filter(location_id), {"$nor": [_build_in_stock_filter(location_id)]}]}


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
