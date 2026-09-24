# ruff: noqa: S101, D100, D101, D102, D103
"""Guards the OpenAPI shape that generated clients rely on to pick the right response type.

Generated clients try `anyOf` members in order and return the first `from_dict` that doesn't raise, and the base
`Product` schema tolerates unknown keys. So the WithVariants types must come first and must *require* `variants`,
otherwise an `include=variants` response silently parses as a plain `Product`.
"""

import pytest

_PRODUCT_SCHEMAS = ["ProductWithVariants", "PartialProductWithVariants", "Product", "PartialProduct"]


@pytest.fixture
def openapi(api_client):
    return api_client.get("/openapi.json").json()


def _ref_names(any_of: list[dict]) -> list[str]:
    return [member["$ref"].rsplit("/", 1)[-1] for member in any_of]


@pytest.mark.parametrize("schema", ["ProductWithVariants", "PartialProductWithVariants"])
def test_variants_is_required(openapi, schema):
    assert "variants" in openapi["components"]["schemas"][schema]["required"]


def test_get_product_union_order(openapi):
    schema = openapi["paths"]["/api/v1/products/{store_id}/{product_id}"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]

    assert _ref_names(schema["anyOf"]) == _PRODUCT_SCHEMAS


def test_list_products_union_order(openapi):
    schema = openapi["paths"]["/api/v1/products/{store_id}"]["get"]["responses"]["200"]["content"]["application/json"][
        "schema"
    ]

    assert _ref_names(schema["anyOf"]) == [f"PaginatedResponse_{name}_" for name in _PRODUCT_SCHEMAS]
