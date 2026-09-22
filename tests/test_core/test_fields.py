# ruff: noqa: S101, D100, D101, D102, D103
"""Tests for core.fields module."""

import pytest
from fastapi import HTTPException

from src.core.fields import FieldsParams, projection_model, to_partial
from src.domain.types.bundles import Bundle, PartialBundle
from src.domain.types.categories import Category, PartialCategory
from src.domain.types.locations import Location, PartialLocation
from src.domain.types.products import PartialProduct, Product
from src.domain.types.stores import PartialStore, Store
from src.domain.types.variants import PartialProductVariant, ProductVariant


@pytest.mark.parametrize(
    ("model", "partial"),
    [
        (Product, PartialProduct),
        (Store, PartialStore),
        (Category, PartialCategory),
        (Location, PartialLocation),
        (ProductVariant, PartialProductVariant),
        (Bundle, PartialBundle),
    ],
)
class TestPartialSchemaParity:
    """Guards against a `PartialX` schema drifting from its full `X` schema (e.g. a forgotten new field)."""

    def test_same_field_names(self, model, partial):
        assert set(partial.model_fields) == set(model.model_fields)

    def test_only_id_is_required(self, model, partial):
        required = {name for name, field in partial.model_fields.items() if field.is_required()}
        assert required == {"id"}


class TestFieldsParamsResolve:
    """`resolve()` is pure Python (no I/O), so these exercise it directly without a running app or Mongo."""

    def test_no_param_returns_none(self):
        assert FieldsParams(fields=None).resolve(Product) is None

    def test_include_top_level(self):
        selection = FieldsParams(fields="name,brand").resolve(Product)

        assert selection.mode == "include"
        assert selection.paths == {("name",), ("brand",)}
        assert selection.fetch_names(Product) == {"name", "brand", "id"}

    def test_exclude_top_level(self):
        selection = FieldsParams(fields="-attributes,-seo").resolve(Product)

        assert selection.mode == "exclude"
        assert selection.fetch_names(Product) == set(Product.model_fields) - {"attributes", "seo"} | {"id"}

    def test_nested_include_path(self):
        selection = FieldsParams(fields="attributes.roast_level").resolve(Product)

        assert selection.mode == "include"
        assert selection.nested_paths("attributes") == [("roast_level",)]
        # include mode only fetches the named top-level fields, unlike exclude mode below
        assert selection.fetch_names(Product) == {"attributes", "id"}

    def test_nested_exclude_path_is_kept_relative_to_its_top_level_field(self):
        selection = FieldsParams(fields="-attributes.roast_level").resolve(Product)

        assert selection.mode == "exclude"
        assert selection.nested_paths("attributes") == [("roast_level",)]
        # the field itself must still be fetched fully so the nested key can be trimmed after the fact
        assert "attributes" in selection.fetch_names(Product)

    def test_whole_field_mention_overrides_a_nested_one(self):
        selection = FieldsParams(fields="attributes,attributes.roast_level").resolve(Product)

        assert selection.nested_paths("attributes") == []

    @pytest.mark.parametrize(
        "fields",
        [
            "",  # empty param
            "name,,brand",  # empty token between commas
            "name,-brand",  # mixed include/exclude
            "nope",  # unknown top-level field
            "-nope",  # unknown top-level field, excluded
            "seo.nope",  # unknown field on a fixed sub-model
            "name.nope",  # drilling into a scalar/leaf field
            "nope.sub",  # unknown top-level field with a nested path
            "-name,seo.slug",  # mixed mode, even with one path nested
            "seo.",  # trailing dot
            ".slug",  # leading dot
            "-",  # bare dash, nothing to exclude
        ],
    )
    def test_invalid_fields_raise_422(self, fields):
        with pytest.raises(HTTPException) as exc_info:
            FieldsParams(fields=fields).resolve(Product)

        assert exc_info.value.status_code == 422


class TestProjectionModel:
    """Also pure Python: no Mongo needed to check the shape Beanie will build its query from."""

    def test_field_names_match_and_id_gets_the_mongo_alias(self):
        model = projection_model(Product, frozenset({"id", "name", "attributes"}))

        assert set(model.model_fields) == {"id", "name", "attributes"}
        assert model.model_fields["id"].alias == "_id"

    def test_populates_from_a_mongo_style_dict(self):
        """Check the model actually accepts that shape.

        Motor hands back raw docs keyed by `_id`, not `id` — `populate_by_name` alone isn't enough
        to prove this works.
        """
        model = projection_model(Product, frozenset({"id", "name"}))

        instance = model.model_validate({"_id": "507f1f77bcf86cd799439011", "name": "Coffee"})

        assert str(instance.id) == "507f1f77bcf86cd799439011"
        assert instance.name == "Coffee"
        assert instance.model_fields_set == {"id", "name"}


class TestToPartial:
    """Check `to_partial` (and the private `_trim` it delegates to for nested paths) without Mongo.

    Builds the same shape `query.project(projection_model(...)).first_or_none()` would return, by hand.
    """

    def test_only_fetched_fields_are_set(self):
        doc = projection_model(Product, frozenset({"id", "name"})).model_validate(
            {"_id": "507f1f77bcf86cd799439011", "name": "Coffee"}
        )

        partial = to_partial(PartialProduct, doc)

        assert partial.model_fields_set == {"id", "name"}
        assert partial.name == "Coffee"
        assert partial.attributes is None

    def test_nested_include_trims_the_container(self):
        selection = FieldsParams(fields="attributes.roast").resolve(Product)
        doc = projection_model(Product, selection.fetch_names(Product)).model_validate(
            {
                "_id": "507f1f77bcf86cd799439011",
                "attributes": {
                    "roast": {"type": "string", "name": "roast", "value": "light"},
                    "organic": {"type": "bool", "name": "organic", "value": True},
                },
            }
        )

        partial = to_partial(PartialProduct, doc, selection)

        assert set(partial.attributes) == {"roast"}

    def test_nested_exclude_trims_the_container(self):
        selection = FieldsParams(fields="-attributes.organic").resolve(Product)
        doc = projection_model(Product, selection.fetch_names(Product)).model_validate(
            {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Coffee",
                "attributes": {
                    "roast": {"type": "string", "name": "roast", "value": "light"},
                    "organic": {"type": "bool", "name": "organic", "value": True},
                },
            }
        )

        partial = to_partial(PartialProduct, doc, selection)

        assert set(partial.attributes) == {"roast"}
        assert partial.name == "Coffee"
