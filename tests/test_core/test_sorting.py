# ruff: noqa: S101, D100, D101, D102, D103
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest
from beanie import PydanticObjectId
from bson import Decimal128
from fastapi import HTTPException

from src.core.sorting import (
    DEFAULT_SORT,
    SortKey,
    SortSpec,
    decode_sort_cursor,
    encode_sort_cursor,
    extract_sort_value,
    keyset_filter,
    parse_sort,
)

ALLOWED = ("name", "created_at")


class TestParseSort:
    def test_none_is_default(self):
        assert parse_sort(None, ALLOWED) == DEFAULT_SORT

    def test_multiple_keys_with_directions(self):
        spec = parse_sort("-created_at,name", ALLOWED)
        assert spec.keys == (SortKey("created_at", True), SortKey("name", False))
        assert spec.signature == "-created_at,name"

    @pytest.mark.parametrize("raw", ["", "name,", "-", "unknown", "name,name", "name,-name", "name,created_at,name"])
    def test_invalid_raises_422(self, raw):
        with pytest.raises(HTTPException) as exc:
            parse_sort(raw, ALLOWED)
        assert exc.value.status_code == 422

    def test_too_many_keys_raises_422(self):
        with pytest.raises(HTTPException) as exc:
            parse_sort("a,b,c,d", ("a", "b", "c", "d"))
        assert exc.value.status_code == 422


class TestSortArgs:
    def test_default_is_id_ascending(self):
        assert DEFAULT_SORT.sort_args() == ["+_id"]
        assert DEFAULT_SORT.sort_args(reverse=True) == ["-_id"]

    def test_id_follows_last_key_direction(self):
        spec = parse_sort("name,-created_at", ALLOWED)
        assert spec.sort_args() == ["+name", "-created_at", "-_id"]
        assert spec.sort_args(reverse=True) == ["-name", "+created_at", "+_id"]


class TestKeysetFilter:
    def test_default_matches_legacy_id_condition(self):
        oid = PydanticObjectId()
        assert keyset_filter(DEFAULT_SORT, [], oid, forward=True) == {"_id": {"$gt": oid}}
        assert keyset_filter(DEFAULT_SORT, [], oid, forward=False) == {"_id": {"$lt": oid}}

    def test_two_keys_mixed_directions_forward(self):
        oid = PydanticObjectId()
        spec = SortSpec((SortKey("name", False), SortKey("created_at", True)))
        assert keyset_filter(spec, ["a", 5], oid, forward=True) == {
            "$or": [
                {"name": {"$gt": "a"}},
                {"name": "a", "created_at": {"$lt": 5}},
                {"name": "a", "created_at": 5, "_id": {"$lt": oid}},
            ]
        }

    def test_backward_inverts_operators(self):
        oid = PydanticObjectId()
        spec = SortSpec((SortKey("name", False),))
        assert keyset_filter(spec, ["a"], oid, forward=False) == {
            "$or": [{"name": {"$lt": "a"}}, {"name": "a", "_id": {"$lt": oid}}]
        }


class TestSortCursor:
    def test_default_cursor_is_legacy_id_cursor(self):
        doc = SimpleNamespace(id=PydanticObjectId())
        cursor = encode_sort_cursor(DEFAULT_SORT, doc)
        assert decode_sort_cursor(cursor, DEFAULT_SORT) == ([], doc.id)

    def test_round_trip_with_datetime_and_string(self):
        spec = parse_sort("-created_at,name", ALLOWED)
        doc = SimpleNamespace(id=PydanticObjectId(), created_at=datetime(2026, 1, 2, 3, 4, 5, 678000), name="x")
        values, oid = decode_sort_cursor(encode_sort_cursor(spec, doc), spec)
        assert values == [doc.created_at, "x"]
        assert oid == doc.id

    def test_signature_mismatch_raises_400(self):
        doc = SimpleNamespace(id=PydanticObjectId(), name="x")
        cursor = encode_sort_cursor(parse_sort("name", ALLOWED), doc)
        for other in (DEFAULT_SORT, parse_sort("-name", ALLOWED)):
            with pytest.raises(HTTPException) as exc:
                decode_sort_cursor(cursor, other)
            assert exc.value.status_code == 400

    def test_legacy_cursor_with_explicit_sort_raises_400(self):
        cursor = encode_sort_cursor(DEFAULT_SORT, SimpleNamespace(id=PydanticObjectId()))
        with pytest.raises(HTTPException) as exc:
            decode_sort_cursor(cursor, parse_sort("name", ALLOWED))
        assert exc.value.status_code == 400

    def test_garbage_raises_400(self):
        with pytest.raises(HTTPException) as exc:
            decode_sort_cursor("!!!not-valid-base64!!!", DEFAULT_SORT)
        assert exc.value.status_code == 400


class TestDynamicSortKeys:
    def test_attr_key_resolves_to_value_path(self):
        (key,) = parse_sort("-attr:weight", ALLOWED, ("attr",)).keys
        assert (key.field, key.path, key.descending, key.nullable) == (
            "attr:weight",
            "attributes.weight.value",
            True,
            True,
        )
        assert key.root == "attributes"

    @pytest.mark.parametrize(
        ("raw", "path"),
        [
            ("price:retail", "price.retail.value"),
            ("region:US:retail", "region_price.US.retail.value"),
            ("loc:abc123:retail", "location_price.abc123.retail.value"),
        ],
    )
    def test_price_keys(self, raw, path):
        assert parse_sort(raw, ALLOWED, ("price", "region", "loc")).keys[0].path == path

    @pytest.mark.parametrize("raw", ["attr:", "attr:a.b", "attr:$x", "region:US", "region:US:", "loc::k"])
    def test_malformed_raises_422(self, raw):
        with pytest.raises(HTTPException) as exc:
            parse_sort(raw, ALLOWED, ("attr", "region", "loc"))
        assert exc.value.status_code == 422

    def test_kind_not_enabled_for_resource_raises_422(self):
        with pytest.raises(HTTPException) as exc:
            parse_sort("price:retail", ALLOWED, ("attr",))
        assert exc.value.status_code == 422

    def test_fields_lists_roots_for_projection(self):
        spec = parse_sort("attr:a,attr:b,price:p", ALLOWED, ("attr", "price"))
        assert spec.fields == ("attributes", "price")


class TestNullableKeyset:
    SPEC = SortSpec((SortKey("attr:w", False, path="attributes.w.value", nullable=True),))

    def test_after_non_null_value(self):
        oid = PydanticObjectId()
        assert keyset_filter(self.SPEC, [5], oid, forward=True) == {
            "$or": [
                {"attributes.w.value": {"$gt": 5}},
                {"attributes.w.value": 5, "_id": {"$gt": oid}},
            ]
        }

    def test_after_null_value_moves_into_non_null_group(self):
        oid = PydanticObjectId()
        assert keyset_filter(self.SPEC, [None], oid, forward=True) == {
            "$or": [
                {"attributes.w.value": {"$ne": None}},
                {"attributes.w.value": None, "_id": {"$gt": oid}},
            ]
        }

    def test_before_non_null_value_includes_nulls(self):
        oid = PydanticObjectId()
        assert keyset_filter(self.SPEC, [5], oid, forward=False) == {
            "$or": [
                {"$or": [{"attributes.w.value": {"$lt": 5}}, {"attributes.w.value": None}]},
                {"attributes.w.value": 5, "_id": {"$lt": oid}},
            ]
        }

    def test_before_null_value_only_stays_within_null_group(self):
        oid = PydanticObjectId()
        assert keyset_filter(self.SPEC, [None], oid, forward=False) == {
            "attributes.w.value": None,
            "_id": {"$lt": oid},
        }


class TestDynamicCursor:
    def test_extracts_from_models_and_dicts_and_round_trips_decimal(self):
        spec = parse_sort("price:retail,attr:n", ALLOWED, ("price", "attr"))
        entry = SimpleNamespace(value=Decimal("12.50"))
        doc = SimpleNamespace(id=PydanticObjectId(), price={"retail": entry}, attributes={"n": {"value": 3}})
        values, _ = decode_sort_cursor(encode_sort_cursor(spec, doc), spec)
        assert values == [Decimal128("12.50"), 3]

    def test_missing_value_encodes_as_null(self):
        spec = parse_sort("attr:n", ALLOWED, ("attr",))
        doc = SimpleNamespace(id=PydanticObjectId(), attributes={})
        assert decode_sort_cursor(encode_sort_cursor(spec, doc), spec)[0] == [None]

    def test_object_id_keyed_map_matches_string_segment(self):
        loc = PydanticObjectId()
        doc = SimpleNamespace(location_price={loc: {"retail": SimpleNamespace(value=1)}})
        assert extract_sort_value(doc, f"location_price.{loc}.retail.value") == 1
