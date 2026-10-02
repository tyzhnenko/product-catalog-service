# ruff: noqa: S101, D100, D101, D102, D103
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from types import SimpleNamespace

from beanie import PydanticObjectId
from bson import Decimal128

from src.core.sorting import (
    DEFAULT_SORT,
    SortKey,
    SortSpec,
    decode_sort_cursor,
    describe_sort,
    encode_sort_cursor,
    extract_sort_value,
)


class Status(str, Enum):
    ACTIVE = "active"


class TestExtractSortValue:
    def test_enum_becomes_its_value(self):
        assert extract_sort_value(SimpleNamespace(status=Status.ACTIVE), "status") == "active"

    def test_decimal_becomes_decimal128(self):
        assert extract_sort_value(SimpleNamespace(v=Decimal("1.50")), "v") == Decimal128("1.50")

    def test_date_becomes_midnight_datetime(self):
        assert extract_sort_value(SimpleNamespace(d=date(2026, 1, 2)), "d") == datetime(2026, 1, 2)

    def test_datetime_is_left_alone(self):
        moment = datetime(2026, 1, 2, 3, 4, 5)
        assert extract_sort_value(SimpleNamespace(d=moment), "d") == moment

    def test_walks_attributes_and_dicts(self):
        doc = SimpleNamespace(attributes={"w": SimpleNamespace(value=3)})
        assert extract_sort_value(doc, "attributes.w.value") == 3

    def test_missing_anywhere_on_the_path_is_none(self):
        doc = SimpleNamespace(attributes={})
        assert extract_sort_value(doc, "attributes.w.value") is None
        assert extract_sort_value(doc, "nope.w.value") is None
        assert extract_sort_value(SimpleNamespace(attributes={"w": None}), "attributes.w.value") is None


class TestSortKeyAndSpec:
    def test_str_marks_descending(self):
        assert str(SortKey("name")) == "name"
        assert str(SortKey("name", True)) == "-name"

    def test_path_defaults_to_field_and_root_is_first_segment(self):
        key = SortKey("name")
        assert (key.path, key.root, key.nullable) == ("name", "name", False)
        assert SortKey("attr:w", path="attributes.w.value", nullable=True).root == "attributes"

    def test_default_spec(self):
        assert DEFAULT_SORT.signature == ""
        assert DEFAULT_SORT.fields == ()
        assert DEFAULT_SORT.columns == [("_id", False, False)]

    def test_columns_end_with_id_following_last_key(self):
        spec = SortSpec((SortKey("name"), SortKey("created_at", True)))
        assert spec.columns == [("name", False, False), ("created_at", True, False), ("_id", True, False)]


class TestDescribeSort:
    def test_lists_static_then_dynamic_forms(self):
        assert describe_sort(("name",), ("attr", "price", "region", "loc")) == (
            "name, attr:<key>, price:<key>, region:<code>:<key>, loc:<id>:<key>"
        )

    def test_static_only(self):
        assert describe_sort(("name", "created_at")) == "name, created_at"


class TestCursorWithDates:
    def test_date_value_round_trips_as_datetime(self):
        spec = SortSpec((SortKey("d"),))
        doc = SimpleNamespace(id=PydanticObjectId(), d=date(2026, 1, 2))
        values, oid = decode_sort_cursor(encode_sort_cursor(spec, doc), spec)
        assert values == [datetime(2026, 1, 2)]
        assert oid == doc.id
