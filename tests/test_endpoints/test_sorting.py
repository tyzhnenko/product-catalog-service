# ruff: noqa: S101, D100, D101, D102, D103
import pytest


@pytest.fixture
def store(api_client):
    return api_client.post(
        "/api/v1/stores/", json={"name": "Sorting Store", "url": "https://sorting.example.com/"}
    ).json()


@pytest.fixture
def products(api_client, store):
    """Five products; two share the name 'Bravo' so ties must fall back to the _id tie-breaker."""
    created = []
    for name in ["Charlie", "Bravo", "Alpha", "Bravo", "Delta"]:
        payload = {"name": name, "brand": "B", "tags": ["t"], "attributes": {}}
        response = api_client.post(f"/api/v1/products/{store['id']}", json=payload)
        assert response.status_code == 200, response.text
        created.append(response.json())
    return created


def _walk(api_client, url, params, direction="after"):
    """Follow cursors to the end; returns every page's items."""
    pages = []
    cursor_param = "after" if direction == "after" else "before"
    cursor_key = "end_cursor" if direction == "after" else "start_cursor"
    has_more = "has_next" if direction == "after" else "has_prev"
    page_params = dict(params)
    while True:
        body = api_client.get(url, params=page_params).json()
        pages.append(body["items"])
        if not body[has_more]:
            return pages
        page_params = {**params, cursor_param: body[cursor_key]}


class TestSortProducts:
    def test_sort_name_ascending(self, api_client, store, products):
        items = api_client.get(f"/api/v1/products/{store['id']}", params={"sort": "name"}).json()["items"]
        assert [item["name"] for item in items] == ["Alpha", "Bravo", "Bravo", "Charlie", "Delta"]

    def test_sort_name_descending(self, api_client, store, products):
        items = api_client.get(f"/api/v1/products/{store['id']}", params={"sort": "-name"}).json()["items"]
        assert [item["name"] for item in items] == ["Delta", "Charlie", "Bravo", "Bravo", "Alpha"]

    def test_sort_created_at_descending_is_newest_first(self, api_client, store, products):
        items = api_client.get(f"/api/v1/products/{store['id']}", params={"sort": "-created_at"}).json()["items"]
        assert [item["id"] for item in items] == [p["id"] for p in reversed(products)]

    def test_default_order_unchanged(self, api_client, store, products):
        items = api_client.get(f"/api/v1/products/{store['id']}").json()["items"]
        assert [item["id"] for item in items] == [p["id"] for p in products]

    def test_forward_pagination_has_no_duplicates_or_gaps(self, api_client, store, products):
        url = f"/api/v1/products/{store['id']}"
        pages = _walk(api_client, url, {"sort": "name", "limit": 2})
        ids = [item["id"] for page in pages for item in page]
        assert len(pages) == 3
        assert len(ids) == len(set(ids)) == 5
        full = api_client.get(url, params={"sort": "name"}).json()["items"]
        assert ids == [item["id"] for item in full]

    def test_backward_pagination_mirrors_forward(self, api_client, store, products):
        url = f"/api/v1/products/{store['id']}"
        params = {"sort": "-name,created_at", "limit": 2}
        forward = _walk(api_client, url, params)
        # jump to the last page, then walk back
        body = api_client.get(url, params=params).json()
        while body["has_next"]:
            body = api_client.get(url, params={**params, "after": body["end_cursor"]}).json()
        backward_ids = [item["id"] for item in body["items"]]
        while body["has_prev"]:
            body = api_client.get(url, params={**params, "before": body["start_cursor"]}).json()
            backward_ids = [item["id"] for item in body["items"]] + backward_ids
        assert backward_ids == [item["id"] for page in forward for item in page]

    def test_sort_with_fields_not_leaking_sort_field(self, api_client, store, products):
        body = api_client.get(
            f"/api/v1/products/{store['id']}", params={"sort": "-created_at", "fields": "brand", "limit": 2}
        ).json()
        assert all(set(item) == {"id", "brand"} for item in body["items"])
        nxt = api_client.get(
            f"/api/v1/products/{store['id']}",
            params={"sort": "-created_at", "fields": "brand", "limit": 2, "after": body["end_cursor"]},
        ).json()
        assert len(nxt["items"]) == 2

    def test_unknown_sort_field_returns_422(self, api_client, store, products):
        response = api_client.get(f"/api/v1/products/{store['id']}", params={"sort": "brand"})
        assert response.status_code == 422

    def test_cursor_from_other_sort_returns_400(self, api_client, store, products):
        url = f"/api/v1/products/{store['id']}"
        cursor = api_client.get(url, params={"sort": "name", "limit": 2}).json()["end_cursor"]
        response = api_client.get(url, params={"sort": "-name", "after": cursor})
        assert response.status_code == 400
        assert api_client.get(url, params={"after": cursor}).status_code == 400


class TestSortOtherResources:
    def test_stores_sort_name_descending(self, api_client):
        for name in ["S-b", "S-c", "S-a"]:
            api_client.post("/api/v1/stores/", json={"name": name, "url": f"https://{name}.example.com/"})
        items = api_client.get("/api/v1/stores/", params={"sort": "-name"}).json()["items"]
        names = [item["name"] for item in items]
        assert names == sorted(names, reverse=True)

    def test_locations_sort_name(self, api_client, store):
        for name in ["L-b", "L-c", "L-a"]:
            response = api_client.post(f"/api/v1/locations/{store['id']}", json={"name": name, "attributes": {}})
            assert response.status_code == 200, response.text
        url = f"/api/v1/locations/{store['id']}"
        items = api_client.get(url, params={"sort": "name", "limit": 2}).json()
        assert [item["name"] for item in items["items"]] == ["L-a", "L-b"]
        nxt = api_client.get(url, params={"sort": "name", "limit": 2, "after": items["end_cursor"]}).json()
        assert [item["name"] for item in nxt["items"]] == ["L-c"]


def _price(value):
    return {"retail": {"type": "decimal", "name": "Retail", "value": value}}


@pytest.fixture
def variants(api_client, store):
    """Five variants; two have no retail price. Prices are chosen so string order differs from numeric order."""
    product = api_client.post(
        f"/api/v1/products/{store['id']}", json={"name": "P", "tags": ["t"], "attributes": {}}
    ).json()
    url = f"/api/v1/variants/{store['id']}/{product['id']}"
    created = []
    for title, price in [("v10", "10"), ("v2.5", "2.5"), ("none-a", None), ("v30", "30"), ("none-b", None)]:
        payload = {"title": title, "options": [{"name": "Size", "value": title}]}
        if price is not None:
            payload["price"] = _price(price)
            payload["region_price"] = {"US": _price(price)}
        response = api_client.post(url, json=payload)
        assert response.status_code == 200, response.text
        created.append(response.json())
    return url, created


class TestSortByPrice:
    def test_numeric_not_lexicographic_missing_first_ascending(self, api_client, variants):
        url, _ = variants
        titles = [i["title"] for i in api_client.get(url, params={"sort": "price:retail"}).json()["items"]]
        assert titles[:2] == ["none-a", "none-b"]
        assert titles[2:] == ["v2.5", "v10", "v30"]

    def test_descending_puts_missing_last(self, api_client, variants):
        url, _ = variants
        titles = [i["title"] for i in api_client.get(url, params={"sort": "-price:retail"}).json()["items"]]
        assert titles[:3] == ["v30", "v10", "v2.5"]
        assert set(titles[3:]) == {"none-a", "none-b"}

    @pytest.mark.parametrize("sort", ["price:retail", "-price:retail"])
    def test_pagination_across_null_boundary_forward_and_backward(self, api_client, variants, sort):
        url, _ = variants
        params = {"sort": sort, "limit": 2}
        full = [i["id"] for i in api_client.get(url, params={"sort": sort}).json()["items"]]

        forward = [i["id"] for page in _walk(api_client, url, params) for i in page]
        assert forward == full

        body = api_client.get(url, params=params).json()
        while body["has_next"]:
            body = api_client.get(url, params={**params, "after": body["end_cursor"]}).json()
        backward = [i["id"] for i in body["items"]]
        while body["has_prev"]:
            body = api_client.get(url, params={**params, "before": body["start_cursor"]}).json()
            backward = [i["id"] for i in body["items"]] + backward
        assert backward == full

    def test_region_price(self, api_client, variants):
        url, _ = variants
        items = api_client.get(url, params={"sort": "-region:US:retail", "limit": 3}).json()["items"]
        assert [i["title"] for i in items] == ["v30", "v10", "v2.5"]

    def test_with_fields_does_not_leak_price(self, api_client, variants):
        url, _ = variants
        body = api_client.get(url, params={"sort": "price:retail", "fields": "title", "limit": 2}).json()
        assert all(set(i) == {"id", "title"} for i in body["items"])
        nxt = api_client.get(
            url, params={"sort": "price:retail", "fields": "title", "limit": 2, "after": body["end_cursor"]}
        )
        assert [i["title"] for i in nxt.json()["items"]] == ["v2.5", "v10"]

    def test_malformed_key_returns_422(self, api_client, variants):
        url, _ = variants
        assert api_client.get(url, params={"sort": "price:"}).status_code == 422
        assert api_client.get(url, params={"sort": "region:US"}).status_code == 422


class TestSortByAttribute:
    def test_product_integer_attribute(self, api_client, store):
        for name, weight in [("a", 250), ("b", 1000), ("c", None), ("d", 50)]:
            attrs = {} if weight is None else {"weight": {"type": "integer", "name": "weight", "value": weight}}
            payload = {"name": name, "tags": ["t"], "attributes": attrs}
            assert api_client.post(f"/api/v1/products/{store['id']}", json=payload).status_code == 200
        url = f"/api/v1/products/{store['id']}"
        asc = [i["name"] for i in api_client.get(url, params={"sort": "attr:weight"}).json()["items"]]
        assert asc == ["c", "d", "a", "b"]
        desc = api_client.get(url, params={"sort": "-attr:weight", "limit": 2}).json()
        assert [i["name"] for i in desc["items"]] == ["b", "a"]
        nxt = api_client.get(url, params={"sort": "-attr:weight", "limit": 2, "after": desc["end_cursor"]}).json()
        assert [i["name"] for i in nxt["items"]] == ["d", "c"]

    def test_price_not_available_on_products(self, api_client, store):
        assert api_client.get(f"/api/v1/products/{store['id']}", params={"sort": "price:retail"}).status_code == 422


def _weight(value):
    return {} if value is None else {"weight": {"type": "integer", "name": "weight", "value": value}}


def _titles(response, field="name"):
    assert response.status_code == 200, response.text
    return [item[field] for item in response.json()["items"]]


class TestSortKeysWiring:
    """Each controller accepts exactly the dynamic key kinds listed in its SORT_KEYS."""

    SAMPLES = {
        "attr": "attr:k",
        "price": "price:k",
        "region": "region:US:k",
        "loc": "loc:6abedce6bcfd2edaecdf5d0a:k",
    }
    ACCEPTED = {
        "stores": set(),
        "categories": {"attr"},
        "locations": {"attr"},
        "products": {"attr"},
        "variants": {"attr", "price", "region", "loc"},
        "bundles": {"attr", "price", "region", "loc"},
    }

    @pytest.fixture
    def urls(self, api_client, store):
        product = api_client.post(
            f"/api/v1/products/{store['id']}", json={"name": "P", "tags": ["t"], "attributes": {}}
        ).json()
        return {
            "stores": "/api/v1/stores/",
            "categories": f"/api/v1/categories/{store['id']}",
            "locations": f"/api/v1/locations/{store['id']}",
            "products": f"/api/v1/products/{store['id']}",
            "variants": f"/api/v1/variants/{store['id']}/{product['id']}",
            "bundles": f"/api/v1/bundles/{store['id']}",
        }

    @pytest.mark.parametrize("resource", list(ACCEPTED))
    @pytest.mark.parametrize("kind", list(SAMPLES))
    def test_kind_accepted_only_where_enabled(self, api_client, urls, resource, kind):
        response = api_client.get(urls[resource], params={"sort": self.SAMPLES[kind]})
        assert response.status_code == (200 if kind in self.ACCEPTED[resource] else 422), response.text


class TestSortKeysPerResource:
    def test_variants_attribute_and_location_price(self, api_client, store):
        product = api_client.post(
            f"/api/v1/products/{store['id']}", json={"name": "P", "tags": ["t"], "attributes": {}}
        ).json()
        location = api_client.post(f"/api/v1/locations/{store['id']}", json={"name": "L", "attributes": {}}).json()
        url = f"/api/v1/variants/{store['id']}/{product['id']}"
        for title, weight, price in [("a", 30, "9.5"), ("b", 5, None), ("c", None, "100"), ("d", 12, "20")]:
            payload = {"title": title, "options": [{"name": "Size", "value": title}], "attributes": _weight(weight)}
            if price is not None:
                payload["location_price"] = {location["id"]: _price(price)}
            assert api_client.post(url, json=payload).status_code == 200

        assert _titles(api_client.get(url, params={"sort": "attr:weight"}), "title") == ["c", "b", "d", "a"]
        by_loc = api_client.get(url, params={"sort": f"-loc:{location['id']}:retail", "limit": 2})
        assert _titles(by_loc, "title") == ["c", "d"]
        nxt = api_client.get(
            url, params={"sort": f"-loc:{location['id']}:retail", "limit": 2, "after": by_loc.json()["end_cursor"]}
        )
        assert _titles(nxt, "title") == ["a", "b"]

    def test_bundles_price_and_attribute(self, api_client, store):
        url = f"/api/v1/bundles/{store['id']}"
        for name, weight, price in [("a", 30, "9.5"), ("b", 5, None), ("c", None, "100"), ("d", 12, "20")]:
            payload = {"name": name, "attributes": _weight(weight)}
            if price is not None:
                payload["price"] = _price(price)
                payload["region_price"] = {"US": _price(price)}
            assert api_client.post(url, json=payload).status_code == 200, name

        assert _titles(api_client.get(url, params={"sort": "price:retail"})) == ["b", "a", "d", "c"]
        assert _titles(api_client.get(url, params={"sort": "-region:US:retail"}))[:3] == ["c", "d", "a"]
        assert _titles(api_client.get(url, params={"sort": "attr:weight"})) == ["c", "b", "d", "a"]

    def test_categories_attribute(self, api_client, store):
        url = f"/api/v1/categories/{store['id']}"
        for name, weight in [("a", 30), ("b", 5), ("c", None)]:
            payload = {"name": name, "status": "active", "path": f"/{name}", "attributes": _weight(weight)}
            assert api_client.post(url, json=payload).status_code == 200, name
        assert _titles(api_client.get(url, params={"sort": "attr:weight"})) == ["c", "b", "a"]
        page = api_client.get(url, params={"sort": "-attr:weight", "limit": 2})
        assert _titles(page) == ["a", "b"]
        nxt = api_client.get(url, params={"sort": "-attr:weight", "limit": 2, "after": page.json()["end_cursor"]})
        assert _titles(nxt) == ["c"]

    def test_locations_attribute(self, api_client, store):
        url = f"/api/v1/locations/{store['id']}"
        for name, weight in [("a", 30), ("b", 5), ("c", None)]:
            assert api_client.post(url, json={"name": name, "attributes": _weight(weight)}).status_code == 200, name
        assert _titles(api_client.get(url, params={"sort": "attr:weight"})) == ["c", "b", "a"]
        page = api_client.get(url, params={"sort": "-attr:weight", "limit": 2})
        assert _titles(page) == ["a", "b"]
        back = api_client.get(url, params={"sort": "-attr:weight", "before": page.json()["end_cursor"], "limit": 2})
        assert _titles(back) == ["a"]
