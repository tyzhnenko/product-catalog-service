# ruff: noqa: S101, D100, D101, D102, D103
import pytest


def _without_timestamps(item: dict) -> dict:
    """Mongo truncates datetimes to milliseconds, so create/read timestamps differ in precision."""
    return {key: value for key, value in item.items() if key not in ("created_at", "updated_at")}


@pytest.fixture
def store(api_client):
    response = api_client.post("/api/v1/stores/", json={"name": "Fields Store", "url": "https://fields.example.com/"})
    return response.json()


@pytest.fixture
def products(api_client, store):
    created = []
    for index in range(3):
        payload = {
            "name": f"Product {index}",
            "description": "Some description",
            "brand": "Brand",
            "tags": ["tag"],
            "seo": {
                "slug": f"product-{index}",
                "title": "Some Title",
                "description": "Some SEO description",
                "keywords": "coffee",
            },
            "attributes": {
                "roast": {"type": "string", "name": "roast", "value": "light"},
                "organic": {"type": "bool", "name": "organic", "value": True},
            },
        }
        created.append(api_client.post(f"/api/v1/products/{store['id']}", json=payload).json())
    return created


class TestProductFields:
    def test_get_include(self, api_client, store, products):
        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "name,brand"}
        )

        assert response.status_code == 200
        assert response.json() == {"id": products[0]["id"], "name": "Product 0", "brand": "Brand"}

    def test_get_exclude(self, api_client, store, products):
        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "-attributes,-seo"}
        )

        assert response.status_code == 200
        body = response.json()
        assert "attributes" not in body
        assert "seo" not in body
        assert body["id"] == products[0]["id"]
        assert body["name"] == "Product 0"
        assert body["created_at"]

    def test_get_without_fields_is_unchanged(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}")

        assert response.status_code == 200
        assert _without_timestamps(response.json()) == _without_timestamps(products[0])

    def test_list_include(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}", params={"fields": "name"})

        assert response.status_code == 200
        body = response.json()
        assert body["items"] == [{"id": product["id"], "name": product["name"]} for product in products]
        assert body["total"] == 3

    def test_list_exclude(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}", params={"fields": "-attributes"})

        assert response.status_code == 200
        assert all("attributes" not in item and "name" in item for item in response.json()["items"])

    def test_list_pagination_with_fields(self, api_client, store, products):
        first = api_client.get(f"/api/v1/products/{store['id']}", params={"fields": "name", "limit": 2}).json()
        assert [item["name"] for item in first["items"]] == ["Product 0", "Product 1"]
        assert first["has_next"] is True

        second = api_client.get(
            f"/api/v1/products/{store['id']}", params={"fields": "name", "limit": 2, "after": first["end_cursor"]}
        ).json()
        assert [item["name"] for item in second["items"]] == ["Product 2"]

    def test_list_without_fields_is_unchanged(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}")

        assert response.status_code == 200
        assert [_without_timestamps(item) for item in response.json()["items"]] == [
            _without_timestamps(product) for product in products
        ]

    @pytest.mark.parametrize(
        "fields",
        [
            "name,-brand",
            "nope",
            "-nope",
            "name,,brand",
            "",
            "seo.nope",  # unknown field on a fixed sub-model
            "name.nope",  # drilling into a scalar/leaf field
            "nope.sub",  # unknown top-level field with a nested path
            "-name,seo.slug",  # mixed mode, even with one path nested
            "seo.",  # trailing dot
            ".slug",  # leading dot
        ],
    )
    def test_invalid_fields(self, api_client, store, products, fields):
        response = api_client.get(f"/api/v1/products/{store['id']}", params={"fields": fields})

        assert response.status_code == 422


class TestProductNestedFields:
    def test_get_nested_include_on_submodel(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "seo.slug"})

        assert response.status_code == 200
        assert response.json() == {"id": products[0]["id"], "seo": {"slug": "product-0"}}

    def test_get_nested_exclude_on_submodel(self, api_client, store, products):
        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "-seo.title"}
        )

        assert response.status_code == 200
        body = response.json()
        assert body["seo"] == {
            "slug": "product-0",
            "description": "Some SEO description",
            "keywords": "coffee",
        }
        assert body["name"] == "Product 0"

    def test_get_nested_include_on_dynamic_map(self, api_client, store, products):
        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "attributes.roast"}
        )

        assert response.status_code == 200
        body = response.json()
        assert set(body["attributes"]) == {"roast"}
        assert body["id"] == products[0]["id"]

    def test_get_nested_exclude_on_dynamic_map(self, api_client, store, products):
        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "-attributes.organic"}
        )

        assert response.status_code == 200
        body = response.json()
        assert set(body["attributes"]) == {"roast"}
        assert body["name"] == "Product 0"

    def test_whole_field_mention_overrides_nested_one(self, api_client, store, products):
        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"fields": "attributes,attributes.roast"}
        )

        assert response.status_code == 200
        assert set(response.json()["attributes"]) == {"roast", "organic"}

    def test_list_nested_include(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}", params={"fields": "attributes.roast"})

        assert response.status_code == 200
        assert all(set(item["attributes"]) == {"roast"} for item in response.json()["items"])
