# ruff: noqa: S101, D100, D101, D102, D103
import pytest


def _without_timestamps(item: dict) -> dict:
    """Mongo truncates datetimes to milliseconds, so create/read timestamps differ in precision."""
    return {key: value for key, value in item.items() if key not in ("created_at", "updated_at")}


@pytest.fixture
def store(api_client):
    response = api_client.post("/api/v1/stores/", json={"name": "Include Store", "url": "https://include.example.com/"})
    return response.json()


@pytest.fixture
def another_store(api_client):
    response = api_client.post(
        "/api/v1/stores/", json={"name": "Another Include Store", "url": "https://include2.example.com/"}
    )
    return response.json()


@pytest.fixture
def products(api_client, store):
    created = []
    for index in range(3):
        payload = {"name": f"Product {index}", "tags": ["tag"]}
        created.append(api_client.post(f"/api/v1/products/{store['id']}", json=payload).json())
    return created


def _create_variant(api_client, store, product, title="Variant"):
    payload = {"title": title, "options": [{"name": "Size", "value": title}]}
    return api_client.post(f"/api/v1/variants/{store['id']}/{product['id']}", json=payload).json()


class TestProductIncludeVariants:
    def test_get_without_include_is_unchanged(self, api_client, store, products):
        _create_variant(api_client, store, products[0])

        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}")

        assert response.status_code == 200
        assert "variants" not in response.json()
        assert _without_timestamps(response.json()) == _without_timestamps(products[0])

    def test_list_without_include_is_unchanged(self, api_client, store, products):
        _create_variant(api_client, store, products[0])

        response = api_client.get(f"/api/v1/products/{store['id']}")

        assert response.status_code == 200
        assert all("variants" not in item for item in response.json()["items"])

    def test_get_with_include_embeds_variants(self, api_client, store, products):
        variant = _create_variant(api_client, store, products[0])

        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"include": "variants"})

        assert response.status_code == 200
        body = response.json()
        assert _without_timestamps(body) == {**_without_timestamps(products[0]), "variants": [variant]}

    def test_get_with_include_and_no_variants_returns_empty_list(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"include": "variants"})

        assert response.status_code == 200
        assert response.json()["variants"] == []

    def test_list_with_include_embeds_variants_per_product(self, api_client, store, products):
        variant0 = _create_variant(api_client, store, products[0], title="V0")
        variant1a = _create_variant(api_client, store, products[1], title="V1a")
        variant1b = _create_variant(api_client, store, products[1], title="V1b")

        response = api_client.get(f"/api/v1/products/{store['id']}", params={"include": "variants"})

        assert response.status_code == 200
        items = {item["id"]: item["variants"] for item in response.json()["items"]}
        assert items[products[0]["id"]] == [variant0]
        assert {v["id"] for v in items[products[1]["id"]]} == {variant1a["id"], variant1b["id"]}
        assert items[products[2]["id"]] == []

    def test_include_excludes_soft_deleted_variants(self, api_client, store, products):
        variant = _create_variant(api_client, store, products[0], title="Keep")
        deleted = _create_variant(api_client, store, products[0], title="Delete me")
        api_client.delete(f"/api/v1/variants/{store['id']}/{products[0]['id']}/{deleted['id']}")

        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"include": "variants"})

        assert response.status_code == 200
        assert [v["id"] for v in response.json()["variants"]] == [variant["id"]]

    def test_include_does_not_leak_variants_across_stores(self, api_client, store, another_store, products):
        other_product = api_client.post(f"/api/v1/products/{another_store['id']}", json={"name": "Other"}).json()
        _create_variant(api_client, another_store, other_product, title="Other store variant")

        response = api_client.get(f"/api/v1/products/{store['id']}/{products[0]['id']}", params={"include": "variants"})

        assert response.status_code == 200
        assert response.json()["variants"] == []

    def test_include_composes_with_fields(self, api_client, store, products):
        _create_variant(api_client, store, products[0], title="V0")

        response = api_client.get(
            f"/api/v1/products/{store['id']}/{products[0]['id']}",
            params={"include": "variants", "fields": "name"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == products[0]["id"]
        assert body["name"] == "Product 0"
        assert "tags" not in body
        assert len(body["variants"]) == 1
        assert body["variants"][0]["title"] == "V0"

    def test_list_pagination_with_include(self, api_client, store, products):
        variant0 = _create_variant(api_client, store, products[0], title="V0")

        first = api_client.get(f"/api/v1/products/{store['id']}", params={"include": "variants", "limit": 2}).json()
        assert first["items"][0]["variants"] == [variant0]
        assert first["has_next"] is True

        second = api_client.get(
            f"/api/v1/products/{store['id']}",
            params={"include": "variants", "limit": 2, "after": first["end_cursor"]},
        ).json()
        assert [item["id"] for item in second["items"]] == [products[2]["id"]]
        assert second["items"][0]["variants"] == []

    @pytest.mark.parametrize("include", ["bogus", "variants,bogus", ","])
    def test_invalid_include(self, api_client, store, products, include):
        response = api_client.get(f"/api/v1/products/{store['id']}", params={"include": include})

        assert response.status_code == 422
