# ruff: noqa: S101, D100, D101, D102, D103
from src.core.fields import FieldSelection, _trim


class TestTrim:
    DATA = {"a": {"b": 1, "c": 2}, "x": 3}

    def test_non_dict_container_is_returned_as_is(self):
        assert _trim(5, [("a",)], "include") == 5
        assert _trim(["a"], [("a",)], "exclude") == ["a"]

    def test_include_keeps_only_named_nested_paths(self):
        assert _trim(self.DATA, [("a", "b")], "include") == {"a": {"b": 1}}

    def test_include_skips_keys_that_are_not_present(self):
        assert _trim(self.DATA, [("zz",), ("a",)], "include") == {"a": {"b": 1, "c": 2}}

    def test_exclude_drops_named_nested_paths(self):
        assert _trim(self.DATA, [("a", "b")], "exclude") == {"a": {"c": 2}, "x": 3}

    def test_exclude_drops_whole_keys(self):
        assert _trim(self.DATA, [("x",)], "exclude") == {"a": {"b": 1, "c": 2}}

    def test_exclude_skips_keys_that_are_not_present(self):
        assert _trim(self.DATA, [("zz",), ("zz", "y")], "exclude") == self.DATA

    def test_exclude_does_not_mutate_the_input(self):
        data = {"a": {"b": 1, "c": 2}}
        _trim(data, [("a", "b")], "exclude")
        assert data == {"a": {"b": 1, "c": 2}}


class TestFieldSelectionSelects:
    def test_id_is_always_selected(self):
        assert FieldSelection("include", frozenset({("name",)})).selects("id")
        assert FieldSelection("exclude", frozenset({("name",)})).selects("id")

    def test_include_mode_selects_only_named_roots(self):
        selection = FieldSelection("include", frozenset({("seo", "slug"), ("name",)}))
        assert selection.selects("seo")
        assert selection.selects("name")
        assert not selection.selects("brand")

    def test_exclude_mode_drops_only_whole_field_mentions(self):
        selection = FieldSelection("exclude", frozenset({("brand",), ("seo", "slug")}))
        assert not selection.selects("brand")
        assert selection.selects("seo")
        assert selection.selects("name")

    def test_fetch_names_adds_extra_fields(self):
        selection = FieldSelection("include", frozenset({("name",)}))
        assert selection.fetch_names(object, extra=["created_at"]) == {"id", "name", "created_at"}
