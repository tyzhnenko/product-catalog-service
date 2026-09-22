# ruff: noqa: S101, D100, D101, D102, D103
"""`fields` coverage for stores/categories/locations/variants/bundles.

Generic mechanics (basic include/exclude, 422s, pagination, whole-field-wins-over-nested) are already covered
end to end for products in `test_fields.py` and at the unit level in `tests/test_core/test_fields.py`. This
file focuses on what's specific to each resource: its own dynamic-map shapes, in particular the doubly-nested
`location_price`/`region_price` maps on variants and bundles.
"""

import pytest


@pytest.fixture
def store(api_client):
    response = api_client.post("/api/v1/stores/", json={"name": "Fields Store", "url": "https://fields.example.com/"})
    return response.json()


class TestStoreFields:
    @pytest.fixture
    def stores(self, api_client):
        return [
            api_client.post(
                "/api/v1/stores/",
                json={
                    "name": f"Store {index}",
                    "url": f"https://store{index}.example.com/",
                    "seo": {
                        "slug": f"store-{index}",
                        "title": "A Title",
                        "description": "A description",
                        "keywords": "coffee",
                    },
                },
            ).json()
            for index in range(2)
        ]

    def test_get_include(self, api_client, stores):
        response = api_client.get(f"/api/v1/stores/{stores[0]['id']}", params={"fields": "name"})

        assert response.status_code == 200
        assert response.json() == {"id": stores[0]["id"], "name": "Store 0"}

    def test_get_exclude(self, api_client, stores):
        response = api_client.get(f"/api/v1/stores/{stores[0]['id']}", params={"fields": "-seo"})

        assert response.status_code == 200
        body = response.json()
        assert "seo" not in body
        assert body["name"] == "Store 0"

    def test_get_nested_include_on_submodel(self, api_client, stores):
        response = api_client.get(f"/api/v1/stores/{stores[0]['id']}", params={"fields": "seo.slug"})

        assert response.status_code == 200
        assert response.json() == {"id": stores[0]["id"], "seo": {"slug": "store-0"}}

    def test_get_nested_exclude_on_submodel(self, api_client, stores):
        response = api_client.get(f"/api/v1/stores/{stores[0]['id']}", params={"fields": "-seo.title"})

        assert response.status_code == 200
        assert response.json()["seo"] == {"slug": "store-0", "description": "A description", "keywords": "coffee"}

    def test_list_include(self, api_client, stores):
        response = api_client.get("/api/v1/stores/", params={"fields": "name"})

        assert response.status_code == 200
        ids = {item["id"] for item in response.json()["items"]}
        assert {store["id"] for store in stores} <= ids
        assert all(set(item) == {"id", "name"} for item in response.json()["items"] if item["id"] in ids)

    def test_get_without_fields_is_unchanged(self, api_client, stores):
        response = api_client.get(f"/api/v1/stores/{stores[0]['id']}")

        assert response.status_code == 200
        assert response.json() == stores[0]


class TestCategoryFields:
    @pytest.fixture
    def categories(self, api_client, store):
        created = []
        for index in range(2):
            payload = {
                "name": f"Category {index}",
                "path": f"/category-{index}",
                "attributes": {
                    "featured": {"type": "bool", "name": "featured", "value": True},
                    "sort_order": {"type": "integer", "name": "sort_order", "value": index},
                },
            }
            created.append(api_client.post(f"/api/v1/categories/{store['id']}", json=payload).json())
        return created

    def test_get_include(self, api_client, store, categories):
        response = api_client.get(f"/api/v1/categories/{store['id']}/{categories[0]['id']}", params={"fields": "name"})

        assert response.status_code == 200
        assert response.json() == {"id": categories[0]["id"], "name": "Category 0"}

    def test_get_nested_include_on_dynamic_map(self, api_client, store, categories):
        response = api_client.get(
            f"/api/v1/categories/{store['id']}/{categories[0]['id']}", params={"fields": "attributes.featured"}
        )

        assert response.status_code == 200
        assert set(response.json()["attributes"]) == {"featured"}

    def test_get_nested_exclude_on_dynamic_map(self, api_client, store, categories):
        response = api_client.get(
            f"/api/v1/categories/{store['id']}/{categories[0]['id']}", params={"fields": "-attributes.sort_order"}
        )

        assert response.status_code == 200
        body = response.json()
        assert set(body["attributes"]) == {"featured"}
        assert body["name"] == "Category 0"

    def test_list_exclude(self, api_client, store, categories):
        response = api_client.get(f"/api/v1/categories/{store['id']}", params={"fields": "-attributes"})

        assert response.status_code == 200
        assert all("attributes" not in item and "name" in item for item in response.json()["items"])


class TestLocationFields:
    @pytest.fixture
    def locations(self, api_client, store):
        created = []
        for index in range(2):
            payload = {
                "name": f"Location {index}",
                "attributes": {
                    "city": {"type": "string", "name": "city", "value": "Seattle"},
                    "zip": {"type": "string", "name": "zip", "value": "98101"},
                },
                "seo": {"slug": f"location-{index}"},
            }
            created.append(api_client.post(f"/api/v1/locations/{store['id']}", json=payload).json())
        return created

    def test_get_include_store_id(self, api_client, store, locations):
        response = api_client.get(
            f"/api/v1/locations/{store['id']}/{locations[0]['id']}", params={"fields": "store_id"}
        )

        assert response.status_code == 200
        assert response.json() == {"id": locations[0]["id"], "store_id": store["id"]}

    def test_get_nested_exclude_on_dynamic_map(self, api_client, store, locations):
        response = api_client.get(
            f"/api/v1/locations/{store['id']}/{locations[0]['id']}", params={"fields": "-attributes.zip"}
        )

        assert response.status_code == 200
        assert set(response.json()["attributes"]) == {"city"}

    def test_list_include(self, api_client, store, locations):
        response = api_client.get(f"/api/v1/locations/{store['id']}", params={"fields": "name"})

        assert response.status_code == 200
        assert all(set(item) == {"id", "name"} for item in response.json()["items"])


class TestVariantFields:
    @pytest.fixture
    def product(self, api_client, store):
        return api_client.post(f"/api/v1/products/{store['id']}", json={"name": "Coffee", "tags": ["tag"]}).json()

    @pytest.fixture
    def location(self, api_client, store):
        return api_client.post(f"/api/v1/locations/{store['id']}", json={"name": "Warehouse"}).json()

    @pytest.fixture
    def variant(self, api_client, store, product, location):
        payload = {
            "title": "Variant",
            "options": [{"name": "size", "value": "large"}],
            "price": {
                "retail": {"type": "decimal", "name": "Retail", "value": "10.00"},
                "wholesale": {"type": "decimal", "name": "Wholesale", "value": "8.00"},
            },
            "location_price": {
                location["id"]: {
                    "retail": {"type": "decimal", "name": "Retail", "value": "12.00"},
                    "member": {"type": "decimal", "name": "Member", "value": "9.00"},
                }
            },
        }
        return api_client.post(f"/api/v1/variants/{store['id']}/{product['id']}", json=payload).json()

    def test_get_nested_include_on_price_map(self, api_client, store, product, variant):
        response = api_client.get(
            f"/api/v1/variants/{store['id']}/{product['id']}/{variant['id']}", params={"fields": "price.retail"}
        )

        assert response.status_code == 200
        assert set(response.json()["price"]) == {"retail"}

    def test_get_nested_exclude_on_doubly_nested_location_price(self, api_client, store, product, variant, location):
        response = api_client.get(
            f"/api/v1/variants/{store['id']}/{product['id']}/{variant['id']}",
            params={"fields": f"-location_price.{location['id']}.member"},
        )

        assert response.status_code == 200
        body = response.json()
        assert set(body["location_price"][location["id"]]) == {"retail"}
        assert body["title"] == "Variant"

    def test_get_nested_include_on_doubly_nested_location_price(self, api_client, store, product, variant, location):
        response = api_client.get(
            f"/api/v1/variants/{store['id']}/{product['id']}/{variant['id']}",
            params={"fields": f"location_price.{location['id']}.retail"},
        )

        assert response.status_code == 200
        body = response.json()
        assert set(body["location_price"][location["id"]]) == {"retail"}
        assert "price" not in body

    def test_list_nested_include(self, api_client, store, product, variant):
        response = api_client.get(f"/api/v1/variants/{store['id']}/{product['id']}", params={"fields": "price.retail"})

        assert response.status_code == 200
        assert all(set(item["price"]) == {"retail"} for item in response.json()["items"])

    def test_get_without_fields_is_unchanged(self, api_client, store, product, variant):
        response = api_client.get(f"/api/v1/variants/{store['id']}/{product['id']}/{variant['id']}")

        assert response.status_code == 200
        assert response.json() == variant


class TestBundleFields:
    @pytest.fixture
    def location(self, api_client, store):
        return api_client.post(f"/api/v1/locations/{store['id']}", json={"name": "Warehouse"}).json()

    @pytest.fixture
    def bundle(self, api_client, store, location):
        payload = {
            "name": "Bundle",
            "attributes": {
                "season": {"type": "string", "name": "season", "value": "winter"},
                "limited": {"type": "bool", "name": "limited", "value": True},
            },
            "location_price": {
                location["id"]: {
                    "retail": {"type": "decimal", "name": "Retail", "value": "20.00"},
                }
            },
        }
        return api_client.post(f"/api/v1/bundles/{store['id']}", json=payload).json()

    def test_get_nested_include_on_dynamic_map(self, api_client, store, bundle):
        response = api_client.get(
            f"/api/v1/bundles/{store['id']}/{bundle['id']}", params={"fields": "attributes.season"}
        )

        assert response.status_code == 200
        assert set(response.json()["attributes"]) == {"season"}

    def test_get_nested_include_on_doubly_nested_location_price(self, api_client, store, bundle, location):
        response = api_client.get(
            f"/api/v1/bundles/{store['id']}/{bundle['id']}",
            params={"fields": f"location_price.{location['id']}.retail"},
        )

        assert response.status_code == 200
        assert set(response.json()["location_price"][location["id"]]) == {"retail"}

    def test_list_exclude(self, api_client, store, bundle):
        response = api_client.get(f"/api/v1/bundles/{store['id']}", params={"fields": "-attributes,-location_price"})

        assert response.status_code == 200
        assert all(
            "attributes" not in item and "location_price" not in item and "name" in item
            for item in response.json()["items"]
        )
