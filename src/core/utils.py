import os
from itertools import accumulate
from pathlib import Path


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
