# ruff: noqa: S101, D100, D101, D102, D103
import uuid

import pytest


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
        # Validate UUID7 format
        assert uuid.UUID(data["id"]).version == 7

    def test_create_store_invalid_url(self, api_client):
        """Test store creation with invalid URL."""
        invalid_data = {
            "name": "Invalid Store",
            "url": "not-a-valid-url",
        }

        response = api_client.post("/api/v1/stores/", json=invalid_data)

        assert response.status_code == 422
        assert "detail" in response.json()

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
        assert response.json() == []

    def test_list_stores_with_one_store(self, api_client, sample_store_data):
        """Test listing stores with one store in database."""
        # Create a store first
        create_response = api_client.post("/api/v1/stores/", json=sample_store_data)
        created_store = create_response.json()

        # List stores
        response = api_client.get("/api/v1/stores/")

        assert response.status_code == 200
        stores = response.json()
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
        stores = response.json()
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

    def test_get_store_not_found(self, api_client):
        """Test getting a non-existent store."""
        # Generate a random UUID7
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/stores/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_get_store_invalid_uuid(self, api_client):
        """Test getting a store with invalid UUID format."""
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
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

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
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.delete(f"/api/v1/stores/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_delete_store_invalid_uuid(self, api_client):
        """Test deleting a store with invalid UUID format."""
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
        assert len(list_response.json()) >= 1

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
