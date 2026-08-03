# ruff: noqa: S101, D100, D101, D102, D103
"""Tests for core.utils module."""

import base64
from decimal import Decimal

import pytest
from beanie import PydanticObjectId
from fastapi import HTTPException

from src.core.utils import (
    build_attribute_filter,
    build_location_price_filter,
    build_region_price_filter,
    decode_cursor,
    encode_cursor,
    split_path,
)


class TestSplitPath:
    """Tests for the split_path function."""

    def test_absolute_path_with_multiple_segments(self):
        """Test splitting an absolute path with multiple segments."""
        result = split_path("/electronics/laptops")
        assert result == ["/", "/electronics", "/electronics/laptops"]

    def test_absolute_path_with_single_segment(self):
        """Test splitting an absolute path with a single segment."""
        result = split_path("/electronics")
        assert result == ["/", "/electronics"]

    def test_root_path(self):
        """Test splitting the root path."""
        result = split_path("/")
        assert result == ["/"]

    def test_relative_path_with_multiple_segments(self):
        """Test splitting a relative path with multiple segments."""
        result = split_path("electronics/laptops/gaming")
        assert result == ["electronics", "electronics/laptops", "electronics/laptops/gaming"]

    def test_relative_path_with_single_segment(self):
        """Test splitting a relative path with a single segment."""
        result = split_path("electronics")
        assert result == ["electronics"]

    def test_path_with_current_directory(self):
        """Test splitting a path starting with current directory marker."""
        result = split_path("./electronics/laptops")
        # Path normalizes away the current directory marker
        assert result == ["electronics", "electronics/laptops"]

    def test_path_with_parent_directory(self):
        """Test splitting a path with parent directory markers."""
        result = split_path("../electronics/laptops")
        assert result == ["..", "../electronics", "../electronics/laptops"]

    def test_empty_string(self):
        """Test splitting an empty string."""
        result = split_path("")
        # Path("") has no parts, so accumulate returns an empty list
        assert result == []

    def test_path_with_trailing_slash(self):
        """Test splitting a path with a trailing slash."""
        result = split_path("/electronics/laptops/")
        # Path normalizes trailing slashes, so this should be same as without trailing slash
        assert result == ["/", "/electronics", "/electronics/laptops"]

    def test_deep_nested_path(self):
        """Test splitting a deeply nested path."""
        result = split_path("/a/b/c/d/e")
        assert result == ["/", "/a", "/a/b", "/a/b/c", "/a/b/c/d", "/a/b/c/d/e"]

    def test_relative_deep_nested_path(self):
        """Test splitting a deeply nested relative path."""
        result = split_path("a/b/c/d")
        assert result == ["a", "a/b", "a/b/c", "a/b/c/d"]

    def test_path_with_special_characters(self):
        """Test splitting a path with special characters in names."""
        result = split_path("/products/coffee-beans/premium_blend")
        assert result == [
            "/",
            "/products",
            "/products/coffee-beans",
            "/products/coffee-beans/premium_blend",
        ]


class TestEncodeCursor:
    def test_returns_string(self):
        assert isinstance(encode_cursor(PydanticObjectId()), str)

    def test_urlsafe_characters(self):
        for _ in range(20):
            result = encode_cursor(PydanticObjectId())
            assert "+" not in result
            assert "/" not in result

    def test_roundtrip(self):
        oid = PydanticObjectId()
        assert decode_cursor(encode_cursor(oid)) == oid

    def test_different_ids_produce_different_cursors(self):
        assert encode_cursor(PydanticObjectId()) != encode_cursor(PydanticObjectId())


class TestDecodeCursor:
    def test_valid_cursor(self):
        oid = PydanticObjectId()
        assert decode_cursor(encode_cursor(oid)) == oid

    def test_invalid_cursor_raises_400(self):
        with pytest.raises(HTTPException) as exc:
            decode_cursor("!!!not-valid-base64!!!")
        assert exc.value.status_code == 400
        assert exc.value.detail == "Invalid cursor"

    def test_valid_base64_but_not_objectid_raises_400(self):
        garbage = base64.urlsafe_b64encode(b"not-an-objectid").decode()
        with pytest.raises(HTTPException) as exc:
            decode_cursor(garbage)
        assert exc.value.status_code == 400
        assert exc.value.detail == "Invalid cursor"


class TestBuildAttributeFilter:
    @pytest.mark.parametrize(
        ("attrs", "expected"),
        [
            (
                ["is_featured:true"],
                {"attributes.is_featured.value": True},
            ),
            (
                ["is_featured:false"],
                {"attributes.is_featured.value": False},
            ),
            (
                ["stock:12"],
                {"attributes.stock.value": 12},
            ),
            (
                ["weight:1.5"],
                {"attributes.weight.value": 1.5},
            ),
            (
                ["label:premium"],
                {"attributes.label.value": "premium"},
            ),
            (
                ["invalid-entry", "label:premium"],
                {"attributes.label.value": "premium"},
            ),
            (
                ["color:red", "color:blue"],
                {"attributes.color.value": {"$in": ["red", "blue"]}},
            ),
            (
                ["in_stock:true", "in_stock:false", "size:42"],
                {
                    "attributes.in_stock.value": {"$in": [True, False]},
                    "attributes.size.value": 42,
                },
            ),
        ],
    )
    def test_builds_expected_filter(self, attrs, expected):
        assert build_attribute_filter(attrs) == expected


class TestBuildLocationPriceFilter:
    @pytest.mark.parametrize(
        ("location_price_id", "location_price_key", "location_price_min", "location_price_max", "expected"),
        [
            (None, "retail", Decimal("10"), Decimal("20"), {}),
            (None, None, None, None, {}),
            (
                "loc-1",
                None,
                None,
                None,
                {"location_price.loc-1": {"$exists": True, "$ne": {}}},
            ),
            (
                "loc-1",
                "retail",
                None,
                None,
                {"location_price.loc-1.retail": {"$exists": True}},
            ),
            (
                "loc-1",
                "retail",
                Decimal("10"),
                None,
                {"location_price.loc-1.retail.value": {"$gte": Decimal("10")}},
            ),
            (
                "loc-1",
                "retail",
                None,
                Decimal("20"),
                {"location_price.loc-1.retail.value": {"$lte": Decimal("20")}},
            ),
            (
                "loc-1",
                "retail",
                Decimal("10"),
                Decimal("20"),
                {"location_price.loc-1.retail.value": {"$gte": Decimal("10"), "$lte": Decimal("20")}},
            ),
        ],
    )
    def test_builds_expected_filter(
        self,
        location_price_id,
        location_price_key,
        location_price_min,
        location_price_max,
        expected,
    ):
        assert (
            build_location_price_filter(
                location_price_id,
                location_price_key,
                location_price_min,
                location_price_max,
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("location_price_min", "location_price_max"), [(Decimal("10"), None), (None, Decimal("20"))]
    )
    def test_min_or_max_without_key_raises_400(self, location_price_min, location_price_max):
        with pytest.raises(HTTPException) as exc_info:
            build_location_price_filter("loc-1", None, location_price_min, location_price_max)
        assert exc_info.value.status_code == 400


class TestBuildRegionPriceFilter:
    @pytest.mark.parametrize(
        ("region_price_code", "region_price_key", "region_price_min", "region_price_max", "expected"),
        [
            (None, "retail", Decimal("10"), Decimal("20"), {}),
            (None, None, None, None, {}),
            (
                "us-east",
                None,
                None,
                None,
                {"region_price.us-east": {"$exists": True, "$ne": {}}},
            ),
            ("us-east", "retail", None, None, {"region_price.us-east.retail": {"$exists": True}}),
            (
                "us-east",
                "retail",
                Decimal("10"),
                None,
                {"region_price.us-east.retail.value": {"$gte": Decimal("10")}},
            ),
            (
                "us-east",
                "retail",
                None,
                Decimal("20"),
                {"region_price.us-east.retail.value": {"$lte": Decimal("20")}},
            ),
            (
                "us-east",
                "retail",
                Decimal("10"),
                Decimal("20"),
                {"region_price.us-east.retail.value": {"$gte": Decimal("10"), "$lte": Decimal("20")}},
            ),
        ],
    )
    def test_builds_expected_filter(
        self,
        region_price_code,
        region_price_key,
        region_price_min,
        region_price_max,
        expected,
    ):
        assert (
            build_region_price_filter(
                region_price_code,
                region_price_key,
                region_price_min,
                region_price_max,
            )
            == expected
        )

    @pytest.mark.parametrize(("region_price_min", "region_price_max"), [(Decimal("10"), None), (None, Decimal("20"))])
    def test_min_or_max_without_key_raises_400(self, region_price_min, region_price_max):
        with pytest.raises(HTTPException) as exc_info:
            build_region_price_filter("us-east", None, region_price_min, region_price_max)
        assert exc_info.value.status_code == 400
