import base64
import os
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
    return PaginatedResponse(
        items=items,
        start_cursor=encode_cursor(docs[0].id) if docs else None,
        end_cursor=encode_cursor(docs[-1].id) if docs else None,
        has_next=has_next,
        has_prev=has_prev,
    )
