import operator
from dataclasses import dataclass
from functools import reduce
from typing import Annotated, Any, Literal, TypeAliasType, TypeVar, cast, get_args, get_origin

from beanie import PydanticObjectId
from fastapi import HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, create_model

from src.core.types import PaginatedResponse

ID_FIELD = "id"

T = TypeVar("T", bound=BaseModel)

FieldPath = tuple[str, ...]


def _real_type(annotation: Any) -> Any:
    """Resolve PEP 695 `type X = ...` aliases and `Annotated[...]`/`X | None` wrappers down to the real type.

    Field annotations in this codebase are typically declared via `type X = Annotated[...]` (e.g.
    `AttributesMap`), which `typing.get_origin`/`get_args` can't see through directly — they need
    `TypeAliasType.__value__` first.
    """
    while True:
        if isinstance(annotation, TypeAliasType):
            annotation = annotation.__value__
            continue
        if get_origin(annotation) is Annotated:
            annotation = get_args(annotation)[0]
            continue
        args = get_args(annotation)
        non_none = [arg for arg in args if arg is not type(None)]
        if len(non_none) == 1 and len(args) > len(non_none):
            annotation = non_none[0]
            continue
        return annotation


def _classify(annotation: Any) -> tuple[Literal["submodel", "dynamic", "leaf"], type[BaseModel] | None]:
    """Classify a field's annotation for nested `fields` path validation.

    "submodel": a fixed-shape `BaseModel` (e.g. `SEO`) — its own fields can be validated recursively.
    "dynamic": a `dict` (e.g. `AttributesMap`, `LocationPriceMap`) — keys are store-defined data, not schema,
    so anything past this point in a path is accepted without validation.
    "leaf": a scalar/list/enum — a path cannot go any deeper here.
    """
    real = _real_type(annotation)
    origin = get_origin(real)
    if origin is dict:
        return "dynamic", None
    if isinstance(real, type) and issubclass(real, BaseModel):
        return "submodel", real
    return "leaf", None


@dataclass(frozen=True)
class _FieldToken:
    """One parsed `fields` token, e.g. `-attributes.roast_level` -> path=("attributes", "roast_level"), exclude=True."""

    path: FieldPath
    exclude: bool

    @classmethod
    def parse(cls, token: str) -> "_FieldToken":
        """Split a raw token into its `-` flag and dotted path.

        Raises:
            HTTPException: 422 if the token (or a dotted segment of it) is empty.

        """
        exclude = token.startswith("-")
        raw = token[1:] if exclude else token
        segments = raw.split(".")
        if not raw or not all(segments):
            raise _invalid(f"Invalid field path in `fields`: {token!r}")
        return cls(path=tuple(segments), exclude=exclude)


def _validate_path(model: type[BaseModel], path: FieldPath, token: str) -> None:
    name, *rest = path
    if name not in model.model_fields:
        raise _invalid(f"Unknown field in `fields`: {token!r}")
    if not rest:
        return

    kind, submodel = _classify(model.model_fields[name].annotation)
    if kind == "leaf":
        raise _invalid(f"'{name}' has no nested fields, invalid path in `fields`: {token!r}")
    if kind == "dynamic":
        return  # opaque past this point: keys are store-defined data, not part of the schema
    _validate_path(cast(type[BaseModel], submodel), tuple(rest), token)  # kind == "submodel"


@dataclass(frozen=True)
class FieldSelection:
    """Resolved `fields` selection; `id` is always kept.

    `paths` holds every parsed path (without its `-`), all include or all exclude per `mode`. A single-segment
    path (`"seo"`) selects/drops a field as a whole; a longer one (`"seo", "slug"`) addresses a nested key and
    is applied after the top-level field is fetched (see `nested_paths`).
    """

    mode: Literal["include", "exclude"]
    paths: frozenset[FieldPath]

    def fetch_names(self, model: type[BaseModel]) -> frozenset[str]:
        """Top-level field names to fetch from Mongo; nested selection is applied after fetching."""
        if self.mode == "include":
            names = {path[0] for path in self.paths}
        else:
            whole_excludes = {path[0] for path in self.paths if len(path) == 1}
            names = set(model.model_fields) - whole_excludes
        return frozenset(names | {ID_FIELD})

    def nested_paths(self, name: str) -> list[FieldPath]:
        """Sub-paths to trim within a fetched top-level field; empty if it should be kept/dropped whole."""
        if any(path == (name,) for path in self.paths):
            return []  # a whole-field mention always wins over any co-occurring nested one
        return [path[1:] for path in self.paths if path[0] == name and len(path) > 1]


@dataclass
class FieldsParams:
    fields: str | None = Query(
        None,
        description=(
            "Comma-separated response fields. Bare names include only those fields (`name,brand`); "
            "`-` prefixed names exclude them (`-seo,-attributes`). Mixing both is not allowed. "
            "Dotted paths address nested fields (`seo.slug`, `-attributes.roast_level`); keys inside "
            "store-defined maps such as `attributes`, `location_price` and `region_price` are not "
            "validated, since they aren't part of the fixed schema. `id` is always returned."
        ),
    )

    def resolve(self, model: type[BaseModel]) -> FieldSelection | None:
        """Validate the raw param against a response model and return the fields to keep.

        Args:
            model: Response schema whose fields (and, for nested paths, sub-schemas) are selectable.

        Returns:
            The selection, or None when no `fields` param was given (all fields).

        Raises:
            HTTPException: 422 on empty, unknown, or mixed include/exclude paths.

        """
        if self.fields is None:
            return None

        tokens = [token.strip() for token in self.fields.split(",")]
        if not tokens or not all(tokens):
            raise _invalid("Empty field name in `fields`")

        included: set[FieldPath] = set()
        excluded: set[FieldPath] = set()
        for token in tokens:
            parsed = _FieldToken.parse(token)
            _validate_path(model, parsed.path, token)
            (excluded if parsed.exclude else included).add(parsed.path)

        if included and excluded:
            raise _invalid("`fields` cannot mix included and excluded (-) names")

        mode: Literal["include", "exclude"] = "include" if included else "exclude"
        return FieldSelection(mode=mode, paths=frozenset(included or excluded))


def _invalid(detail: str) -> HTTPException:
    return HTTPException(status_code=422, detail=detail)


def projection_model(model: type[BaseModel], names: frozenset[str]) -> Any:
    """Build the Beanie projection model that fetches a set of top-level fields; `id` maps to Mongo `_id`.

    Fields are untyped on purpose: Beanie only needs the names to build the projection, and the values are
    validated afterwards against the resource's `PartialX` response schema (see `to_partial`).
    """
    definitions: dict[str, Any] = {name: (Any, None) for name in names if name != ID_FIELD}
    definitions[ID_FIELD] = (PydanticObjectId, Field(..., alias="_id"))
    return create_model(
        f"{model.__name__}Projection",
        __config__=ConfigDict(populate_by_name=True),
        **definitions,
    )


def _trim(container: Any, sub_paths: list[FieldPath], mode: Literal["include", "exclude"]) -> Any:
    """Keep (include) or drop (exclude) the given sub-paths inside a fetched nested dict, recursively."""
    if not isinstance(container, dict):
        return container

    grouped: dict[str, list[FieldPath]] = {}
    for path in sub_paths:
        grouped.setdefault(path[0], []).append(path[1:])

    if mode == "include":
        result: dict[str, Any] = {}
        for key, rest_paths in grouped.items():
            if key not in container:
                continue
            deeper = [path for path in rest_paths if path]
            result[key] = _trim(container[key], deeper, mode) if deeper else container[key]
        return result

    result = dict(container)
    for key, rest_paths in grouped.items():
        if key not in result:
            continue
        deeper = [path for path in rest_paths if path]
        if deeper:
            result[key] = _trim(result[key], deeper, mode)
        else:
            del result[key]
    return result


def to_partial(partial: type[T], doc: BaseModel, selection: FieldSelection | None = None) -> T:
    """Convert a projected document into its resource's `PartialX` response schema.

    Only fields present on `doc` (i.e. actually projected) are set. Where `selection` addresses nested paths,
    the matching containers are trimmed to just those paths before validation.
    """
    data = doc.model_dump(exclude_unset=True)
    if selection is not None:
        for name, value in list(data.items()):
            nested = selection.nested_paths(name)
            if nested:
                data[name] = _trim(value, nested, selection.mode)
    return partial.model_validate(data)


def sparse_response(*models: type[BaseModel], paginated: bool = False) -> Any:
    """FastAPI `response_model` for handlers whose response shape depends on request params.

    Takes two or more candidate response schemas (e.g. the full schema and its `fields`-narrowed `PartialX`
    variant) and unions them, since the actual return value's runtime type determines which one it validates
    against. For `paginated`, each candidate is unioned as its own fully-parametrized `PaginatedResponse[X]`
    (not a single `PaginatedResponse[X | Y]`), so a page's `items` stay one homogeneous shape — matching how
    `paginate()` always parametrizes its result on the single runtime type shared by every item in the page.
    """
    if paginated:
        return reduce(operator.or_, (PaginatedResponse[model] for model in models))  # type: ignore[valid-type]
    return reduce(operator.or_, models)
