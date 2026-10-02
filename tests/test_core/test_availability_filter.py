# ruff: noqa: S101, D100, D101, D102, D103
import pytest
from fastapi import HTTPException

from src.core.utils import _parse_availability, build_availability_filter

LOC = "6abedce6bcfd2edaecdf5d0a"
PRICED_AT_LOC = {f"location_price.{LOC}": {"$exists": True, "$ne": {}}}
IN_STOCK_AT_LOC = {**PRICED_AT_LOC, f"attributes.locations_availability.values.{LOC}": {"$ne": "out_of_stock"}}


class TestParseAvailability:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("in_stock", (None, True)),
            ("out_of_stock", (None, False)),
            (f"loc:{LOC}", (LOC, True)),
            (f"loc:{LOC}:in_stock", (LOC, True)),
            (f"loc:{LOC}:out_of_stock", (LOC, False)),
            (f"loc:{LOC.upper()}", (LOC, True)),
        ],
    )
    def test_valid_values(self, value, expected):
        assert _parse_availability(value) == expected

    @pytest.mark.parametrize("value", ["", "stock", "loc:", "loc:xyz", f"loc:{LOC}:bogus", f"region:{LOC}"])
    def test_invalid_values_raise_422(self, value):
        with pytest.raises(HTTPException) as exc:
            _parse_availability(value)
        assert exc.value.status_code == 422


class TestBuildAvailabilityFilter:
    def test_none_means_no_filter(self):
        assert build_availability_filter(None) == {}

    def test_in_stock_at_location(self):
        assert build_availability_filter(f"loc:{LOC}") == IN_STOCK_AT_LOC

    def test_out_of_stock_at_location_is_priced_but_not_in_stock(self):
        assert build_availability_filter(f"loc:{LOC}:out_of_stock") == {
            "$and": [PRICED_AT_LOC, {"$nor": [IN_STOCK_AT_LOC]}]
        }

    def test_unscoped_in_stock_is_an_expression_over_priced_locations(self):
        result = build_availability_filter("in_stock")
        assert list(result) == ["$expr"]
        assert "$anyElementTrue" in result["$expr"]

    def test_unscoped_out_of_stock_requires_an_offer_and_negates_in_stock(self):
        priced, negated = build_availability_filter("out_of_stock")["$and"]
        assert priced["$expr"]["$gt"][1] == 0
        assert negated == {"$nor": [build_availability_filter("in_stock")]}

    def test_invalid_value_raises_422(self):
        with pytest.raises(HTTPException) as exc:
            build_availability_filter("nope")
        assert exc.value.status_code == 422
