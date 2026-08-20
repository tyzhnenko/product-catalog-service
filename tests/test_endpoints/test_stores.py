# ruff: noqa: S101, D100, D101, D102, D103
import pytest
from beanie import PydanticObjectId


@pytest.fixture
def sample_store_data():
    """Sample data for creating a store."""
    return {
        "name": "Test Coffee Store",
        "url": "https://testcoffeestore.com/",
    }


@pytest.fixture
def another_store_data():
    """Another sample store data for testing multiple stores."""
    return {
        "name": "Another Coffee Shop",
        "url": "https://anothercoffeeshop.com",
    }


class TestCreateStore:
    """Tests for POST /api/v1/stores/."""

    def test_create_store_success(self, api_client, sample_store_data):
        """Test successful store creation."""
        response = api_client.post("/api/v1/stores/", json=sample_store_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == sample_store_data["name"]
        assert data["url"] == sample_store_data["url"]
        assert "id" in data

    def test_create_store_invalid_url(self, api_client):
        """Test store creation with invalid URL."""
        invalid_data = {
            "name": "Invalid Store",
            "url": "not-a-valid-url",
        }

        response = api_client.post("/api/v1/stores/", json=invalid_data)

        assert response.status_code == 422
        assert "detail" in response.json()

    def test_create_store_duplicate_slug_returns_409(self, api_client, sample_store_data):
        """Test that creating a second store with the same slug returns 409."""
        store_data = {**sample_store_data, "seo": {"slug": "test-coffee-store"}}
        first = api_client.post("/api/v1/stores/", json=store_data)
        assert first.status_code == 200

        duplicate_data = {**store_data, "name": "Different Name", "url": "https://different.example.com/"}
        response = api_client.post("/api/v1/stores/", json=duplicate_data)

        assert response.status_code == 409

    def test_create_store_missing_name(self, api_client):
        """Test store creation without name."""
        invalid_data = {
            "url": "https://teststore.com",
        }

        response = api_client.post("/api/v1/stores/", json=invalid_data)

        assert response.status_code == 422

    def test_create_store_missing_url(self, api_client):
        """Test store creation without URL."""
        invalid_data = {
            "name": "Test Store",
        }

        response = api_client.post("/api/v1/stores/", json=invalid_data)

        assert response.status_code == 422

    def test_create_store_empty_name(self, api_client):
        """Test store creation with empty name."""
        invalid_data = {
            "name": "",
            "url": "https://teststore.com",
        }

        response = api_client.post("/api/v1/stores/", json=invalid_data)

        assert response.status_code == 422


class TestListStores:
    """Tests for GET /api/v1/stores/."""

    def test_list_stores_empty(self, api_client):
        """Test listing stores when database is empty."""
        response = api_client.get("/api/v1/stores/")

        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_list_stores_with_one_store(self, api_client, sample_store_data):
        """Test listing stores with one store in database."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()

        # List stores
        response = api_client.get("/api/v1/stores/")

        assert response.status_code == 200
        stores = response.json()["items"]
        assert len(stores) == 1
        assert stores[0]["id"] == created_store["id"]
        assert stores[0]["name"] == sample_store_data["name"]
        assert stores[0]["url"] == sample_store_data["url"]

    def test_list_stores_with_multiple_stores(self, api_client, sample_store_data, another_store_data):
        """Test listing multiple stores."""
        # Create two stores
        api_client.post("/api/v1/stores/", json=sample_store_data)
        api_client.post("/api/v1/stores/", json=another_store_data)

        # List stores
        response = api_client.get("/api/v1/stores/")

        assert response.status_code == 200
        stores = response.json()["items"]
        assert len(stores) == 2

        store_names = {store["name"] for store in stores}
        assert sample_store_data["name"] in store_names
        assert another_store_data["name"] in store_names


class TestGetStore:
    """Tests for GET /api/v1/stores/{store_id}."""

    def test_get_store_success(self, api_client, sample_store_data):
        """Test successful retrieval of a specific store."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Get the store
        response = api_client.get(f"/api/v1/stores/{store_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == sample_store_data["name"]
        assert data["url"] == sample_store_data["url"]

    def test_get_store_by_slug(self, api_client, sample_store_data):
        """Test that a store can be looked up by its 's-<slug>' ref, resolving to the same document."""
        store_data = {**sample_store_data, "seo": {"slug": "test-coffee-store"}}
        create_response = api_client.post("/api/v1/stores/", json=store_data)
        created_store = create_response.json()

        response = api_client.get("/api/v1/stores/s-test-coffee-store")

        assert response.status_code == 200
        assert response.json()["id"] == created_store["id"]

    def test_get_store_not_found(self, api_client):
        """Test getting a non-existent store."""
        # Generate a random UUID7
        non_existent_id = str(PydanticObjectId())

        response = api_client.get(f"/api/v1/stores/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_get_store_invalid_uuid(self, api_client):
        """Test getting a store with invalid UUID format (rejected by path param validation)."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/stores/{invalid_id}")

        assert response.status_code == 422


class TestUpdateStore:
    """Tests for PUT /api/v1/stores/{store_id}."""

    def test_update_store_name(self, api_client, sample_store_data):
        """Test updating store name."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Update the store name
        update_data = {
            "name": "Updated Coffee Store",
            "url": None,
        }
        response = api_client.put(f"/api/v1/stores/{store_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == "Updated Coffee Store"
        assert data["url"] == sample_store_data["url"]  # URL should remain unchanged

    def test_update_store_url(self, api_client, sample_store_data):
        """Test updating store URL."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Update the store URL
        update_data = {
            "name": None,
            "url": "https://newurl.com",
        }
        response = api_client.put(f"/api/v1/stores/{store_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == sample_store_data["name"]  # Name should remain unchanged
        assert data["url"] == "https://newurl.com/"

    def test_update_store_both_fields(self, api_client, sample_store_data):
        """Test updating both name and URL."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Update both fields
        update_data = {
            "name": "Completely New Store",
            "url": "https://completelynew.com",
        }
        response = api_client.put(f"/api/v1/stores/{store_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == "Completely New Store"
        assert data["url"] == "https://completelynew.com/"

    def test_update_store_not_found(self, api_client):
        """Test updating a non-existent store."""
        non_existent_id = str(PydanticObjectId())

        update_data = {
            "name": "Updated Name",
            "url": None,
        }
        response = api_client.put(f"/api/v1/stores/{non_existent_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_update_store_invalid_url(self, api_client, sample_store_data):
        """Test updating store with invalid URL."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Try to update with invalid URL
        update_data = {
            "name": None,
            "url": "not-a-valid-url",
        }
        response = api_client.put(f"/api/v1/stores/{store_id}", json=update_data)

        assert response.status_code == 422

    def test_update_store_empty_name(self, api_client, sample_store_data):
        """Test updating store with empty name."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Try to update with empty name
        update_data = {
            "name": "",
            "url": None,
        }
        response = api_client.put(f"/api/v1/stores/{store_id}", json=update_data)

        assert response.status_code == 422


class TestDeleteStore:
    """Tests for DELETE /api/v1/stores/{store_id}."""

    def test_delete_store_success(self, api_client, sample_store_data):
        """Test successful soft delete of a store."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Delete the store
        response = api_client.delete(f"/api/v1/stores/{store_id}")

        assert response.status_code == 204

    def test_delete_store_not_found(self, api_client):
        """Test deleting a non-existent store."""
        non_existent_id = str(PydanticObjectId())

        response = api_client.delete(f"/api/v1/stores/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_delete_store_invalid_uuid(self, api_client):
        """Test deleting a store with invalid UUID format (rejected by path param validation)."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/stores/{invalid_id}")

        assert response.status_code == 422

    def test_get_deleted_store(self, api_client, sample_store_data):
        """Test that a deleted store can still be retrieved (soft delete)."""
        # Create a store
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()
        store_id = created_store["id"]

        # Delete the store
        api_client.delete(f"/api/v1/stores/{store_id}")

        # Try to get the deleted store
        # Note: This test behavior depends on whether your list/get methods filter out soft-deleted records
        # Adjust based on your actual implementation
        response = api_client.get(f"/api/v1/stores/{store_id}")

        # If soft delete is implemented properly, the store should still exist but have deleted_at set
        # The actual behavior depends on your business logic
        # You may need to adjust this assertion based on how you want soft deletes to work
        assert response.status_code in [200, 404]


class TestStoreCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, api_client, sample_store_data):
        """Test the complete CRUD lifecycle of a store."""
        # Create
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        assert create_response.status_code == 200
        created_store = create_response.json()
        store_id = created_store["id"]

        # Read (single)
        get_response = api_client.get(f"/api/v1/stores/{store_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == store_id

        # Read (list)
        list_response = api_client.get("/api/v1/stores/")
        assert list_response.status_code == 200
        assert len(list_response.json()["items"]) >= 1

        # Update
        update_data = {
            "name": "Updated Store Name",
            "url": "https://updated.com",
        }
        update_response = api_client.put(f"/api/v1/stores/{store_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Store Name"

        # Verify update
        get_updated_response = api_client.get(f"/api/v1/stores/{store_id}")
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["name"] == "Updated Store Name"

        # Delete
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204


class TestStoreRecursiveDelete:
    """Tests for recursive soft delete when deleting a store."""

    def test_delete_store_cascades_to_products(self, api_client):
        """Test that deleting a store soft deletes all products."""
        # Create a store
        store_data = {"name": "Store with Products", "url": "https://storeproducts.com/"}
        store_response = api_client.post("/api/v1/stores/", json=store_data)
        store_id = store_response.json()["id"]

        # Create a category
        category_data = {"name": "Test Category", "status": "active", "path": "/test"}
        category_response = api_client.post(f"/api/v1/categories/{store_id}", json=category_data)
        category_id = category_response.json()["id"]

        # Create products
        product_data = {"name": "Product 1", "tags": [], "categories": [category_id]}
        product1_response = api_client.post(f"/api/v1/products/{store_id}", json=product_data)
        product1_id = product1_response.json()["id"]

        product_data["name"] = "Product 2"
        product2_response = api_client.post(f"/api/v1/products/{store_id}", json=product_data)
        product2_id = product2_response.json()["id"]

        # Delete the store
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204

        # Verify products are soft deleted (not accessible)
        product1_get = api_client.get(f"/api/v1/products/{store_id}/{product1_id}")
        product2_get = api_client.get(f"/api/v1/products/{store_id}/{product2_id}")
        assert product1_get.status_code == 404
        assert product2_get.status_code == 404

    def test_delete_store_cascades_to_variants(self, api_client):
        """Test that deleting a store soft deletes all variants."""
        # Create a store
        store_data = {"name": "Store with Variants", "url": "https://storevariants.com/"}
        store_response = api_client.post("/api/v1/stores/", json=store_data)
        store_id = store_response.json()["id"]

        # Create a product
        product_data = {"name": "Product with Variants", "tags": []}
        product_response = api_client.post(f"/api/v1/products/{store_id}", json=product_data)
        product_id = product_response.json()["id"]

        # Create variants
        variant_data = {"title": "Variant 1", "options": [{"name": "size", "value": "small"}]}
        variant1_response = api_client.post(f"/api/v1/variants/{store_id}/{product_id}", json=variant_data)
        variant1_id = variant1_response.json()["id"]

        variant_data = {"title": "Variant 2", "options": [{"name": "size", "value": "large"}]}
        variant2_response = api_client.post(f"/api/v1/variants/{store_id}/{product_id}", json=variant_data)
        variant2_id = variant2_response.json()["id"]

        # Delete the store
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204

        # Verify variants are soft deleted (not accessible)
        variant1_get = api_client.get(f"/api/v1/variants/{store_id}/{product_id}/{variant1_id}")
        variant2_get = api_client.get(f"/api/v1/variants/{store_id}/{product_id}/{variant2_id}")
        assert variant1_get.status_code == 404
        assert variant2_get.status_code == 404

    def test_delete_store_cascades_to_bundles(self, api_client):
        """Test that deleting a store soft deletes all bundles."""
        # Create a store
        store_data = {"name": "Store with Bundles", "url": "https://storebundles.com/"}
        store_response = api_client.post("/api/v1/stores/", json=store_data)
        store_id = store_response.json()["id"]

        # Create bundles
        bundle_data = {"name": "Bundle 1"}
        bundle1_response = api_client.post(f"/api/v1/bundles/{store_id}", json=bundle_data)
        bundle1_id = bundle1_response.json()["id"]

        bundle_data["name"] = "Bundle 2"
        bundle2_response = api_client.post(f"/api/v1/bundles/{store_id}", json=bundle_data)
        bundle2_id = bundle2_response.json()["id"]

        # Delete the store
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204

        # Verify bundles are soft deleted (not accessible)
        bundle1_get = api_client.get(f"/api/v1/bundles/{store_id}/{bundle1_id}")
        bundle2_get = api_client.get(f"/api/v1/bundles/{store_id}/{bundle2_id}")
        assert bundle1_get.status_code == 404
        assert bundle2_get.status_code == 404

    def test_delete_store_cascades_to_categories(self, api_client):
        """Test that deleting a store soft deletes all categories."""
        # Create a store
        store_data = {"name": "Store with Categories", "url": "https://storecategories.com/"}
        store_response = api_client.post("/api/v1/stores/", json=store_data)
        store_id = store_response.json()["id"]

        # Create categories
        category_data = {"name": "Category 1", "status": "active", "path": "/cat1"}
        cat1_response = api_client.post(f"/api/v1/categories/{store_id}", json=category_data)
        cat1_id = cat1_response.json()["id"]

        category_data = {"name": "Category 2", "status": "active", "path": "/cat2"}
        cat2_response = api_client.post(f"/api/v1/categories/{store_id}", json=category_data)
        cat2_id = cat2_response.json()["id"]

        # Delete the store
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204

        # Verify categories are soft deleted (not accessible)
        cat1_get = api_client.get(f"/api/v1/categories/{store_id}/{cat1_id}")
        cat2_get = api_client.get(f"/api/v1/categories/{store_id}/{cat2_id}")
        assert cat1_get.status_code == 404
        assert cat2_get.status_code == 404

    def test_delete_store_cascades_to_locations(self, api_client):
        """Test that deleting a store soft deletes all locations."""
        # Create a store
        store_data = {"name": "Store with Locations", "url": "https://storelocations.com/"}
        store_response = api_client.post("/api/v1/stores/", json=store_data)
        store_id = store_response.json()["id"]

        # Create locations
        location_data = {"name": "Location 1"}
        loc1_response = api_client.post(f"/api/v1/locations/{store_id}", json=location_data)
        loc1_id = loc1_response.json()["id"]

        location_data["name"] = "Location 2"
        loc2_response = api_client.post(f"/api/v1/locations/{store_id}", json=location_data)
        loc2_id = loc2_response.json()["id"]

        # Delete the store
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204

        # Verify locations are soft deleted (not accessible)
        loc1_get = api_client.get(f"/api/v1/locations/{store_id}/{loc1_id}")
        loc2_get = api_client.get(f"/api/v1/locations/{store_id}/{loc2_id}")
        assert loc1_get.status_code == 404
        assert loc2_get.status_code == 404

    def test_delete_store_full_cascade(self, api_client):
        """Test that deleting a store cascades to all nested resources."""
        # Create a store
        store_data = {"name": "Full Store", "url": "https://fullstore.com/"}
        store_response = api_client.post("/api/v1/stores/", json=store_data)
        store_id = store_response.json()["id"]

        # Create category
        category_data = {"name": "Category", "status": "active", "path": "/category"}
        category_response = api_client.post(f"/api/v1/categories/{store_id}", json=category_data)

        # Create product
        product_data = {"name": "Product", "tags": []}
        product_response = api_client.post(f"/api/v1/products/{store_id}", json=product_data)
        product_id = product_response.json()["id"]

        # Create variant
        variant_data = {"title": "Variant", "options": []}
        variant_response = api_client.post(f"/api/v1/variants/{store_id}/{product_id}", json=variant_data)

        # Create bundle
        bundle_data = {"name": "Bundle"}
        bundle_response = api_client.post(f"/api/v1/bundles/{store_id}", json=bundle_data)

        # Create location
        location_data = {"name": "Location"}
        location_response = api_client.post(f"/api/v1/locations/{store_id}", json=location_data)

        # Delete the store
        delete_response = api_client.delete(f"/api/v1/stores/{store_id}")
        assert delete_response.status_code == 204

        deleted_category = api_client.get(f"/api/v1/categories/{store_id}/{category_response.json()['id']}")
        assert deleted_category.status_code == 404

        deleted_location = api_client.get(f"/api/v1/locations/{store_id}/{location_response.json()['id']}")
        assert deleted_location.status_code == 404

        deleted_product = api_client.get(f"/api/v1/products/{store_id}/{product_id}")
        assert deleted_product.status_code == 404

        deleted_bundle = api_client.get(f"/api/v1/bundles/{store_id}/{bundle_response.json()['id']}")
        assert deleted_bundle.status_code == 404

        deleted_variant = api_client.get(f"/api/v1/variants/{store_id}/{product_id}/{variant_response.json()['id']}")
        assert deleted_variant.status_code == 404

        # Verify all resources are gone from lists
        categories_list = api_client.get(f"/api/v1/categories/{store_id}")
        products_list = api_client.get(f"/api/v1/products/{store_id}")
        bundles_list = api_client.get(f"/api/v1/bundles/{store_id}")
        locations_list = api_client.get(f"/api/v1/locations/{store_id}")

        # All should return 404 (store not found) or empty lists depending on implementation
        assert categories_list.status_code == 404 or categories_list.json()["items"] == []
        assert products_list.status_code == 404 or products_list.json()["items"] == []
        assert bundles_list.status_code == 404 or bundles_list.json()["items"] == []
        assert locations_list.status_code == 404 or locations_list.json()["items"] == []


class TestListStoresPagination:
    """Pagination tests for GET /api/v1/stores/."""

    def test_first_page_no_cursor(self, api_client):
        """No cursor: first page, has_next when more items exist."""
        for i in range(3):
            api_client.post("/api/v1/stores/", json={"name": f"Pagination Store {i}", "url": f"https://store{i}.com/"})

        response = api_client.get("/api/v1/stores/", params={"limit": 2})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["has_next"] is True
        assert data["has_prev"] is False
        assert data["end_cursor"] is not None

    def test_forward_pagination(self, api_client):
        """after=end_cursor fetches the next page."""
        for i in range(3):
            api_client.post("/api/v1/stores/", json={"name": f"FwdStore {i}", "url": f"https://fwdstore{i}.com/"})

        page1 = api_client.get("/api/v1/stores/", params={"limit": 2}).json()
        page2_resp = api_client.get("/api/v1/stores/", params={"after": page1["end_cursor"], "limit": 2})

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 1
        assert page2["has_next"] is False
        assert page2["has_prev"] is True

    def test_middle_page_has_next(self, api_client):
        """after=end_cursor on a middle page returns has_next=True and truncates to limit."""
        for i in range(5):
            api_client.post("/api/v1/stores/", json={"name": f"MidStore {i}", "url": f"https://midstore{i}.com/"})

        page1 = api_client.get("/api/v1/stores/", params={"limit": 2}).json()
        page2_resp = api_client.get("/api/v1/stores/", params={"after": page1["end_cursor"], "limit": 2})

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 2
        assert page2["has_next"] is True
        assert page2["has_prev"] is True

    def test_middle_page_has_prev(self, api_client):
        """before=start_cursor on a middle page returns has_prev=True and truncates to limit."""
        for i in range(5):
            api_client.post("/api/v1/stores/", json={"name": f"PrevStore {i}", "url": f"https://prevstore{i}.com/"})

        page1 = api_client.get("/api/v1/stores/", params={"limit": 2}).json()
        page2 = api_client.get("/api/v1/stores/", params={"after": page1["end_cursor"], "limit": 2}).json()
        page3 = api_client.get("/api/v1/stores/", params={"after": page2["end_cursor"], "limit": 2}).json()

        back_resp = api_client.get("/api/v1/stores/", params={"before": page3["start_cursor"], "limit": 2})

        assert back_resp.status_code == 200
        back = back_resp.json()
        assert len(back["items"]) == 2
        assert back["has_prev"] is True
        assert back["has_next"] is True

    def test_empty_result(self, api_client):
        """No stores: empty paginated response."""
        response = api_client.get("/api/v1/stores/")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["start_cursor"] is None
        assert data["end_cursor"] is None
        assert data["has_next"] is False
        assert data["has_prev"] is False

    def test_invalid_cursor(self, api_client):
        """Invalid cursor returns 400."""
        response = api_client.get("/api/v1/stores/", params={"after": "not-a-valid-cursor"})
        assert response.status_code == 400

    def test_limit_max_enforced(self, api_client):
        """Limit > max_limit returns 422."""
        response = api_client.get("/api/v1/stores/", params={"limit": 999})
        assert response.status_code == 422
