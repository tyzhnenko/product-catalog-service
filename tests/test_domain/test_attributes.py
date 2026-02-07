# ruff: noqa: S101, D100, D101, D102, D103
"""Tests for domain.types.attributes module."""

from datetime import timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from beanie import PydanticObjectId
from pydantic import ValidationError
from pydantic_extra_types.pendulum_dt import Date, DateTime

from src.domain.types.attributes import (
    BoolAttribute,
    DateAttribute,
    DateTimeAttribute,
    DecimalAttribute,
    DecimalRangeAttribute,
    FloatAttribute,
    FloatRangeAttribute,
    IntegerAttribute,
    IntegerRangeAttribute,
    ListOfDatesAttribute,
    ListOfDateTimesAttribute,
    ListOfDecimalsAttribute,
    ListOfFloatsAttribute,
    ListOfIntegersAttribute,
    ListOfObjectIdsAttribute,
    ListOfStringsAttribute,
    ListOfURLsAttribute,
    ListOfUUIDsAttribute,
    MapOfDatesAttribute,
    MapOfDateTimesAttribute,
    MapOfDecimalsAttribute,
    MapOfFloatsAttribute,
    MapOfIntegersAttribute,
    MapOfObjectIdsAttribute,
    MapOfStringsAttribute,
    MapOfURLsAttribute,
    MapOfUUIDsAttribute,
    ObjectIdAttribute,
    StringAttribute,
    TextAttribute,
    URLAttribute,
    UUIDAttribute,
)


class TestBasicAttributes:
    """Tests for basic attribute types."""

    def test_string_attribute(self):
        """Test StringAttribute creation and validation."""
        attr = StringAttribute(name="color", value="blue")
        assert attr.type == "string"
        assert attr.name == "color"
        assert attr.value == "blue"

    def test_text_attribute(self):
        """Test TextAttribute creation and validation."""
        attr = TextAttribute(name="description", value="This is a long text description")
        assert attr.type == "text"
        assert attr.name == "description"
        assert attr.value == "This is a long text description"

    def test_integer_attribute(self):
        """Test IntegerAttribute creation and validation."""
        attr = IntegerAttribute(name="quantity", value=42)
        assert attr.type == "integer"
        assert attr.name == "quantity"
        assert attr.value == 42

    def test_float_attribute(self):
        """Test FloatAttribute creation and validation."""
        attr = FloatAttribute(name="weight", value=3.14)
        assert attr.type == "float"
        assert attr.name == "weight"
        assert attr.value == 3.14

    def test_decimal_attribute(self):
        """Test DecimalAttribute creation and validation."""
        attr = DecimalAttribute(name="price", value=Decimal("19.99"))
        assert attr.type == "decimal"
        assert attr.name == "price"
        assert attr.value == Decimal("19.99")

    def test_bool_attribute(self):
        """Test BoolAttribute creation and validation."""
        attr = BoolAttribute(name="is_active", value=True)
        assert attr.type == "bool"
        assert attr.name == "is_active"
        assert attr.value is True

    def test_date_attribute(self):
        """Test DateAttribute creation and validation."""
        test_date = Date(2026, 2, 8)
        attr = DateAttribute(name="release_date", value=test_date)
        assert attr.type == "date"
        assert attr.name == "release_date"
        assert attr.value == test_date

    def test_datetime_attribute(self):
        """Test DateTimeAttribute creation and validation."""
        test_datetime = DateTime(2026, 2, 8, 12, 30, 0, tzinfo=timezone.utc)
        attr = DateTimeAttribute(name="created_at", value=test_datetime)
        assert attr.type == "datetime"
        assert attr.name == "created_at"
        assert attr.value == test_datetime

    def test_uuid_attribute(self):
        """Test UUIDAttribute creation and validation."""
        test_uuid = uuid4()
        attr = UUIDAttribute(name="id", value=test_uuid)
        assert attr.type == "uuid"
        assert attr.name == "id"
        assert attr.value == test_uuid

    def test_object_id_attribute(self):
        """Test ObjectIdAttribute creation and validation."""
        test_object_id = PydanticObjectId()
        attr = ObjectIdAttribute(name="reference", value=test_object_id)
        assert attr.type == "object_id"
        assert attr.name == "reference"
        assert attr.value == test_object_id

    def test_url_attribute(self):
        """Test URLAttribute creation and validation."""
        from pydantic import HttpUrl

        attr = URLAttribute(name="website", value=HttpUrl("https://example.com"))
        assert attr.type == "url"
        assert attr.name == "website"
        assert str(attr.value) == "https://example.com/"


class TestRangeAttributes:
    """Tests for range attribute types."""

    def test_float_range_attribute(self):
        """Test FloatRangeAttribute creation and validation."""
        attr = FloatRangeAttribute(name="temperature", min_value=0.0, max_value=100.0)
        assert attr.type == "float_range"
        assert attr.name == "temperature"
        assert attr.min_value == 0.0
        assert attr.max_value == 100.0

    def test_integer_range_attribute(self):
        """Test IntegerRangeAttribute creation and validation."""
        attr = IntegerRangeAttribute(name="age_range", min_value=18, max_value=65)
        assert attr.type == "integer_range"
        assert attr.name == "age_range"
        assert attr.min_value == 18
        assert attr.max_value == 65

    def test_decimal_range_attribute(self):
        """Test DecimalRangeAttribute creation and validation."""
        attr = DecimalRangeAttribute(name="price_range", min_value=Decimal("10.00"), max_value=Decimal("99.99"))
        assert attr.type == "decimal_range"
        assert attr.name == "price_range"
        assert attr.min_value == Decimal("10.00")
        assert attr.max_value == Decimal("99.99")


class TestListAttributes:
    """Tests for list attribute types."""

    def test_list_of_strings_attribute(self):
        """Test ListOfStringsAttribute creation and validation."""
        attr = ListOfStringsAttribute(name="tags", values=["tag1", "tag2", "tag3"])
        assert attr.type == "list_of_strings"
        assert attr.name == "tags"
        assert attr.values == ["tag1", "tag2", "tag3"]

    def test_list_of_integers_attribute(self):
        """Test ListOfIntegersAttribute creation and validation."""
        attr = ListOfIntegersAttribute(name="numbers", values=[1, 2, 3, 4, 5])
        assert attr.type == "list_of_integers"
        assert attr.name == "numbers"
        assert attr.values == [1, 2, 3, 4, 5]

    def test_list_of_floats_attribute(self):
        """Test ListOfFloatsAttribute creation and validation."""
        attr = ListOfFloatsAttribute(name="measurements", values=[1.1, 2.2, 3.3])
        assert attr.type == "list_of_floats"
        assert attr.name == "measurements"
        assert attr.values == [1.1, 2.2, 3.3]

    def test_list_of_decimals_attribute(self):
        """Test ListOfDecimalsAttribute creation and validation."""
        attr = ListOfDecimalsAttribute(name="prices", values=[Decimal("10.99"), Decimal("20.99"), Decimal("30.99")])
        assert attr.type == "list_of_decimals"
        assert attr.name == "prices"
        assert attr.values == [Decimal("10.99"), Decimal("20.99"), Decimal("30.99")]

    def test_list_of_uuids_attribute(self):
        """Test ListOfUUIDsAttribute creation and validation."""
        uuids = [uuid4(), uuid4(), uuid4()]
        attr = ListOfUUIDsAttribute(name="identifiers", values=uuids)
        assert attr.type == "list_of_uuids"
        assert attr.name == "identifiers"
        assert attr.values == uuids

    def test_list_of_object_ids_attribute(self):
        """Test ListOfObjectIdsAttribute creation and validation."""
        object_ids = [PydanticObjectId(), PydanticObjectId(), PydanticObjectId()]
        attr = ListOfObjectIdsAttribute(name="references", values=object_ids)
        assert attr.type == "list_of_object_ids"
        assert attr.name == "references"
        assert attr.values == object_ids

    def test_list_of_urls_attribute(self):
        """Test ListOfURLsAttribute creation and validation."""
        from pydantic import HttpUrl

        attr = ListOfURLsAttribute(
            name="links",
            values=[
                HttpUrl("https://example.com"),
                HttpUrl("https://example.org"),
                HttpUrl("https://example.net"),
            ],
        )
        assert attr.type == "list_of_urls"
        assert attr.name == "links"
        assert len(attr.values) == 3

    def test_list_of_dates_attribute(self):
        """Test ListOfDatesAttribute creation and validation."""
        dates = [Date(2026, 1, 1), Date(2026, 2, 1), Date(2026, 3, 1)]
        attr = ListOfDatesAttribute(name="important_dates", values=dates)
        assert attr.type == "list_of_dates"
        assert attr.name == "important_dates"
        assert attr.values == dates

    def test_list_of_datetimes_attribute(self):
        """Test ListOfDateTimesAttribute creation and validation."""
        datetimes = [
            DateTime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            DateTime(2026, 2, 1, 12, 0, 0, tzinfo=timezone.utc),
            DateTime(2026, 3, 1, 12, 0, 0, tzinfo=timezone.utc),
        ]
        attr = ListOfDateTimesAttribute(name="events", values=datetimes)
        assert attr.type == "list_of_datetimes"
        assert attr.name == "events"
        assert attr.values == datetimes

    def test_empty_list_attribute(self):
        """Test that list attributes can be empty."""
        attr = ListOfStringsAttribute(name="tags", values=[])
        assert attr.type == "list_of_strings"
        assert attr.values == []


class TestMapAttributes:
    """Tests for map attribute types."""

    def test_map_of_strings_attribute(self):
        """Test MapOfStringsAttribute creation and validation."""
        attr = MapOfStringsAttribute(name="labels", values={"key1": "value1", "key2": "value2"})
        assert attr.type == "map_of_strings"
        assert attr.name == "labels"
        assert attr.values == {"key1": "value1", "key2": "value2"}

    def test_map_of_integers_attribute(self):
        """Test MapOfIntegersAttribute creation and validation."""
        attr = MapOfIntegersAttribute(name="counts", values={"apples": 5, "oranges": 10})
        assert attr.type == "map_of_integers"
        assert attr.name == "counts"
        assert attr.values == {"apples": 5, "oranges": 10}

    def test_map_of_floats_attribute(self):
        """Test MapOfFloatsAttribute creation and validation."""
        attr = MapOfFloatsAttribute(name="weights", values={"item1": 1.5, "item2": 2.7})
        assert attr.type == "map_of_floats"
        assert attr.name == "weights"
        assert attr.values == {"item1": 1.5, "item2": 2.7}

    def test_map_of_decimals_attribute(self):
        """Test MapOfDecimalsAttribute creation and validation."""
        attr = MapOfDecimalsAttribute(
            name="prices",
            values={"product1": Decimal("19.99"), "product2": Decimal("29.99")},
        )
        assert attr.type == "map_of_decimals"
        assert attr.name == "prices"
        assert attr.values == {"product1": Decimal("19.99"), "product2": Decimal("29.99")}

    def test_map_of_uuids_attribute(self):
        """Test MapOfUUIDsAttribute creation and validation."""
        uuid1, uuid2 = uuid4(), uuid4()
        attr = MapOfUUIDsAttribute(name="identifiers", values={"first": uuid1, "second": uuid2})
        assert attr.type == "map_of_uuids"
        assert attr.name == "identifiers"
        assert attr.values == {"first": uuid1, "second": uuid2}

    def test_map_of_object_ids_attribute(self):
        """Test MapOfObjectIdsAttribute creation and validation."""
        oid1, oid2 = PydanticObjectId(), PydanticObjectId()
        attr = MapOfObjectIdsAttribute(name="references", values={"ref1": oid1, "ref2": oid2})
        assert attr.type == "map_of_object_ids"
        assert attr.name == "references"
        assert attr.values == {"ref1": oid1, "ref2": oid2}

    def test_map_of_urls_attribute(self):
        """Test MapOfURLsAttribute creation and validation."""
        from pydantic import HttpUrl

        attr = MapOfURLsAttribute(
            name="links",
            values={
                "homepage": HttpUrl("https://example.com"),
                "docs": HttpUrl("https://docs.example.com"),
            },
        )
        assert attr.type == "map_of_urls"
        assert attr.name == "links"
        assert len(attr.values) == 2

    def test_map_of_dates_attribute(self):
        """Test MapOfDatesAttribute creation and validation."""
        attr = MapOfDatesAttribute(
            name="deadlines",
            values={
                "phase1": Date(2026, 3, 1),
                "phase2": Date(2026, 6, 1),
            },
        )
        assert attr.type == "map_of_dates"
        assert attr.name == "deadlines"
        assert attr.values["phase1"] == Date(2026, 3, 1)
        assert attr.values["phase2"] == Date(2026, 6, 1)

    def test_map_of_datetimes_attribute(self):
        """Test MapOfDateTimesAttribute creation and validation."""
        attr = MapOfDateTimesAttribute(
            name="events",
            values={
                "start": DateTime(2026, 1, 1, 9, 0, 0, tzinfo=timezone.utc),
                "end": DateTime(2026, 1, 1, 17, 0, 0, tzinfo=timezone.utc),
            },
        )
        assert attr.type == "map_of_datetimes"
        assert attr.name == "events"
        assert attr.values["start"] == DateTime(2026, 1, 1, 9, 0, 0, tzinfo=timezone.utc)
        assert attr.values["end"] == DateTime(2026, 1, 1, 17, 0, 0, tzinfo=timezone.utc)

    def test_empty_map_attribute(self):
        """Test that map attributes can be empty."""
        attr = MapOfStringsAttribute(name="labels", values={})
        assert attr.type == "map_of_strings"
        assert attr.values == {}


class TestAttributeValidation:
    """Tests for attribute validation."""

    def test_invalid_string_attribute_missing_value(self):
        """Test that StringAttribute requires a value."""
        with pytest.raises(ValidationError):
            StringAttribute(name="color")  # type: ignore

    def test_invalid_integer_attribute_wrong_type(self):
        """Test that IntegerAttribute validates value type."""
        with pytest.raises(ValidationError):
            IntegerAttribute(name="count", value="not_an_integer")  # type: ignore

    def test_invalid_float_attribute_wrong_type(self):
        """Test that FloatAttribute validates value type."""
        with pytest.raises(ValidationError):
            FloatAttribute(name="weight", value="not_a_float")  # type: ignore

    def test_invalid_bool_attribute_wrong_type(self):
        """Test that BoolAttribute validates value type."""
        with pytest.raises(ValidationError):
            BoolAttribute(name="active", value="not_a_bool")  # type: ignore

    def test_invalid_url_attribute(self):
        """Test that URLAttribute validates URL format."""
        with pytest.raises(ValidationError):
            URLAttribute(name="website", value="not-a-valid-url")  # type: ignore

    def test_invalid_list_of_integers_wrong_type(self):
        """Test that ListOfIntegersAttribute validates list item types."""
        with pytest.raises(ValidationError):
            ListOfIntegersAttribute(name="numbers", values=[1, 2, "three"])  # type: ignore

    def test_invalid_map_of_integers_wrong_value_type(self):
        """Test that MapOfIntegersAttribute validates map value types."""
        with pytest.raises(ValidationError):
            MapOfIntegersAttribute(name="counts", values={"key": "not_an_int"})  # type: ignore


class TestAttributeSerialization:
    """Tests for attribute serialization."""

    def test_string_attribute_json_serialization(self):
        """Test StringAttribute serialization to JSON."""
        attr = StringAttribute(name="color", value="blue")
        json_data = attr.model_dump()
        assert json_data == {"type": "string", "name": "color", "value": "blue"}

    def test_list_of_strings_json_serialization(self):
        """Test ListOfStringsAttribute serialization to JSON."""
        attr = ListOfStringsAttribute(name="tags", values=["tag1", "tag2"])
        json_data = attr.model_dump()
        assert json_data == {"type": "list_of_strings", "name": "tags", "values": ["tag1", "tag2"]}

    def test_map_of_strings_json_serialization(self):
        """Test MapOfStringsAttribute serialization to JSON."""
        attr = MapOfStringsAttribute(name="labels", values={"key1": "value1"})
        json_data = attr.model_dump()
        assert json_data == {
            "type": "map_of_strings",
            "name": "labels",
            "values": {"key1": "value1"},
        }

    def test_list_of_dates_json_serialization(self):
        """Test ListOfDatesAttribute serialization to JSON."""
        dates = [Date(2026, 1, 1), Date(2026, 2, 1)]
        attr = ListOfDatesAttribute(name="dates", values=dates)
        json_data = attr.model_dump()
        assert json_data["type"] == "list_of_dates"
        assert json_data["name"] == "dates"
        assert len(json_data["values"]) == 2

    def test_map_of_datetimes_json_serialization(self):
        """Test MapOfDateTimesAttribute serialization to JSON."""
        attr = MapOfDateTimesAttribute(
            name="events",
            values={"event1": DateTime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)},
        )
        json_data = attr.model_dump()
        assert json_data["type"] == "map_of_datetimes"
        assert json_data["name"] == "events"
        assert "event1" in json_data["values"]
