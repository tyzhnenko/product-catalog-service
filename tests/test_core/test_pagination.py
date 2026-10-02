# ruff: noqa: S101, D100, D101, D102, D103
import inspect

import pytest
from fastapi import HTTPException

from src.core.pagination import PaginationParams, pagination_with_sort
from src.core.sorting import DEFAULT_SORT


class TestPaginationParams:
    def test_defaults(self):
        params = PaginationParams()
        assert (params.after, params.before) == (None, None)
        assert params.limit > 0
        assert params.sort == DEFAULT_SORT


class TestPaginationWithSort:
    dependency = staticmethod(pagination_with_sort(("name", "created_at"), ("attr",)))

    def test_builds_params_with_parsed_sort(self):
        params = self.dependency(after="a", before=None, limit=5, sort="-name,attr:weight")
        assert (params.after, params.before, params.limit) == ("a", None, 5)
        assert params.sort.signature == "-name,attr:weight"

    def test_no_sort_is_default_order(self):
        assert self.dependency(after=None, before=None, limit=5, sort=None).sort == DEFAULT_SORT

    def test_invalid_sort_raises_422(self):
        with pytest.raises(HTTPException) as exc:
            self.dependency(after=None, before=None, limit=5, sort="price:retail")
        assert exc.value.status_code == 422

    def test_description_lists_allowed_fields_and_dynamic_forms(self):
        description = inspect.signature(self.dependency).parameters["sort"].default.description
        assert "name, created_at, attr:<key>" in description
        assert "not index-backed" in description

    def test_description_omits_dynamic_notes_without_dynamic_kinds(self):
        description = inspect.signature(pagination_with_sort(("name",))).parameters["sort"].default.description
        assert "name" in description
        assert "index-backed" not in description
