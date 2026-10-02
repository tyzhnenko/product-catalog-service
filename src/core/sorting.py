import base64
import re
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

from beanie import PydanticObjectId
from bson import Binary, Decimal128, json_util
from fastapi import HTTPException

MAX_SORT_KEYS = 3

_LEGACY_CURSOR = re.compile(r"^[0-9a-f]{24}$")

# Dynamic sort keys address a value inside a store-defined map: `<kind>:<segment>[:<segment>]`. Each maps to the
# document's top-level map field and how many `:`-separated segments follow the kind. The sorted value is the
# entry's `value` (so range/list/map entries, which have none, count as missing).
DYNAMIC_KINDS: dict[str, tuple[str, int]] = {
    "attr": ("attributes", 1),
    "price": ("price", 1),
    "region": ("region_price", 2),
    "loc": ("location_price", 2),
}


@dataclass(frozen=True)
class SortKey:
    """One sort column: a document field (or a path into a dynamic map) and its direction.

    `field` is the name as the client wrote it (`name`, `attr:weight`); `path` is the Mongo path it resolves to.
    `nullable` columns (dynamic keys) may be missing/null on some documents; Mongo orders those lowest, i.e.
    first ascending and last descending.
    """

    field: str
    descending: bool = False
    path: str = ""
    nullable: bool = False

    def __post_init__(self) -> None:
        if not self.path:
            object.__setattr__(self, "path", self.field)

    @property
    def root(self) -> str:
        """Top-level document field the value lives in; this is what must be fetched under a projection."""
        return self.path.split(".", 1)[0]

    def __str__(self) -> str:
        return f"-{self.field}" if self.descending else self.field


@dataclass(frozen=True)
class SortSpec:
    """Parsed `sort` param. An empty spec means the default order: `_id` ascending.

    `_id` is always the implicit last column so the order is total, which is what makes keyset cursors
    stable when sort values tie. It follows the direction of the last explicit key.
    """

    keys: tuple[SortKey, ...] = ()

    @property
    def signature(self) -> str:
        return ",".join(str(key) for key in self.keys)

    @property
    def fields(self) -> tuple[str, ...]:
        """Top-level document fields needed to read every sort value."""
        return tuple(dict.fromkeys(key.root for key in self.keys))

    @property
    def id_descending(self) -> bool:
        return self.keys[-1].descending if self.keys else False

    @property
    def columns(self) -> list[tuple[str, bool, bool]]:
        """`(mongo path, descending, nullable)` for every column, ending with the `_id` tie-breaker."""
        return [*((key.path, key.descending, key.nullable) for key in self.keys), ("_id", self.id_descending, False)]

    def sort_args(self, reverse: bool = False) -> list[str]:
        """Beanie `.sort(...)` arguments; `reverse` flips every direction (used for `before` paging)."""
        return [("+" if descending == reverse else "-") + path for path, descending, _ in self.columns]


DEFAULT_SORT = SortSpec()


def parse_sort(raw: str | None, allowed: tuple[str, ...], dynamic: tuple[str, ...] = ()) -> SortSpec:
    """Parse a comma-separated `sort` param, e.g. `-created_at,attr:weight`.

    Args:
        raw: The raw query value.
        allowed: Static, top-level fields the resource can be sorted by.
        dynamic: Dynamic key kinds (see `DYNAMIC_KINDS`) the resource supports, e.g. `("attr", "price")`.

    Raises:
        HTTPException: 422 on empty, unknown, malformed or duplicate fields, or more than `MAX_SORT_KEYS` keys.

    """
    if raw is None:
        return SortSpec()

    keys: list[SortKey] = []
    for token in (part.strip() for part in raw.split(",")):
        descending = token.startswith("-")
        field = token[1:] if descending else token
        if not field:
            raise _invalid("Empty field name in `sort`")
        key = SortKey(field, descending) if field in allowed else _parse_dynamic(field, descending, dynamic)
        if key is None:
            raise _invalid(f"Unknown sort field: {field!r}. Allowed: {describe_sort(allowed, dynamic)}")
        if any(existing.field == key.field for existing in keys):
            raise _invalid(f"Duplicate sort field: {field!r}")
        keys.append(key)

    if len(keys) > MAX_SORT_KEYS:
        raise _invalid(f"`sort` accepts at most {MAX_SORT_KEYS} fields")
    return SortSpec(tuple(keys))


def describe_sort(allowed: tuple[str, ...], dynamic: tuple[str, ...] = ()) -> str:
    """Human-readable list of the accepted sort fields, for error messages and the OpenAPI description."""
    forms = {"attr": "attr:<key>", "price": "price:<key>", "region": "region:<code>:<key>", "loc": "loc:<id>:<key>"}
    return ", ".join([*allowed, *(forms[kind] for kind in dynamic)])


def _parse_dynamic(field: str, descending: bool, dynamic: tuple[str, ...]) -> SortKey | None:
    kind, _, rest = field.partition(":")
    if kind not in dynamic or kind not in DYNAMIC_KINDS:
        return None
    root, count = DYNAMIC_KINDS[kind]
    segments = rest.split(":", count - 1)
    if len(segments) != count or not all(_valid_segment(segment) for segment in segments):
        raise _invalid(f"Malformed sort field: {field!r}. Expected {describe_sort((), (kind,))}")
    return SortKey(field, descending, path=".".join([root, *segments, "value"]), nullable=True)


def _valid_segment(segment: str) -> bool:
    return bool(segment) and not any(char in segment for char in ".$\x00")


def keyset_filter(spec: SortSpec, values: list[Any], cursor_id: PydanticObjectId, forward: bool) -> dict[str, Any]:
    """Mongo condition selecting documents strictly after (`forward`) or before the cursor in `spec` order."""
    columns = spec.columns
    cursor_values = [*values, cursor_id]
    branches: list[dict[str, Any]] = []
    for i, (path, descending, nullable) in enumerate(columns):
        beyond = _beyond(path, cursor_values[i], greater=descending != forward, nullable=nullable)
        if beyond is None:
            continue
        branch: dict[str, Any] = {columns[j][0]: cursor_values[j] for j in range(i)}
        branch.update(beyond)
        branches.append(branch)
    return branches[0] if len(branches) == 1 else {"$or": branches}


def _beyond(path: str, value: Any, greater: bool, nullable: bool) -> dict[str, Any] | None:
    """Condition for a column's value being strictly past `value`; None when nothing can be.

    Null and missing are treated alike and ordered lowest, matching Mongo's own sort. Mongo's range operators
    only match values of the same BSON type as the bound, so null needs explicit handling.
    """
    if not nullable:
        return {path: {"$gt" if greater else "$lt": value}}
    if greater:
        return {path: {"$ne": None}} if value is None else {path: {"$gt": value}}
    if value is None:
        return None
    return {"$or": [{path: {"$lt": value}}, {path: None}]}


def extract_sort_value(doc: Any, path: str) -> Any:
    """Read the value at a (possibly dotted) Mongo path from a model instance, a projection or a plain dict."""
    current = doc
    for segment in path.split("."):
        if current is None:
            return None
        if isinstance(current, dict):
            # Map keys are typed (e.g. ObjectId location ids) on full models, but the path segment is a string.
            current = (
                current[segment]
                if segment in current
                else next((v for k, v in current.items() if str(k) == segment), None)
            )
        else:
            current = getattr(current, segment, None)
    return _to_bson(current)


def _to_bson(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        return Decimal128(value)
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime.combine(value, time.min)
    return value


def encode_sort_cursor(spec: SortSpec, doc: Any) -> str:
    """Cursor for `doc`: the bare `_id` for the default order, else sort values + `_id` as extended JSON."""
    if not spec.keys:
        return base64.urlsafe_b64encode(str(doc.id).encode()).decode()
    payload = {
        "s": spec.signature,
        "v": [extract_sort_value(doc, key.path) for key in spec.keys],
        "id": doc.id,
    }
    return base64.urlsafe_b64encode(json_util.dumps(payload).encode()).decode()


def decode_sort_cursor(cursor: str, spec: SortSpec) -> tuple[list[Any], PydanticObjectId]:
    """Return `(sort values, _id)` from a cursor issued for the same `spec`.

    Raises:
        HTTPException: 400 if the cursor is malformed or was issued for a different `sort`.

    """
    try:
        decoded = base64.urlsafe_b64decode(cursor.encode()).decode()
        if _LEGACY_CURSOR.match(decoded):
            signature, values, cursor_id = "", [], PydanticObjectId(decoded)
        else:
            payload = json_util.loads(decoded)
            signature, values, cursor_id = payload["s"], list(payload["v"]), PydanticObjectId(payload["id"])
    except Exception as ex:
        raise HTTPException(status_code=400, detail="Invalid cursor") from ex

    if signature != spec.signature or len(values) != len(spec.keys):
        raise HTTPException(status_code=400, detail="Cursor does not match the requested sort")
    # json_util revives binary subtype 4 as a UUID, which the driver can't encode without a configured
    # representation; send it back as the binary Beanie stored.
    return [Binary.from_uuid(v) if isinstance(v, UUID) else v for v in values], cursor_id


def _invalid(detail: str) -> HTTPException:
    return HTTPException(status_code=422, detail=detail)
