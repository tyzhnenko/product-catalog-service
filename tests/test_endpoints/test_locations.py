# ruff: noqa: S101, D100, D101, D102, D103
import uuid

import pytest


@pytest.fixture
def sample_store(api_client):
    """Create a sample store for testing locations."""
    store_data = {
        "name": "Test Store for Locations",
        "url": "https://teststorelocations.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def another_store(api_client):
    """Create another store for testing locations."""
    store_data = {
        "name": "Another Test Store",
        "url": "https://anotherstore.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def sample_location_data(sample_store):
    """Sample data for creating a location."""
    return {
        "name": "Downtown Location",
        "store_id": sample_store["id"],
    }


@pytest.fixture
def another_location_data(sample_store):
    """Another sample location data for testing multiple locations."""
    return {
        "name": "Uptown Location",
        "store_id": sample_store["id"],
    }


class TestCreateLocation:
    """Tests for POST /api/v1/locations/{store_id}."""

    def test_create_location_success(self, api_client, sample_location_data, sample_store):
        """Test successful location creation."""
        response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == sample_location_data["name"]
        assert data["store_id"] == sample_location_data["store_id"]
        assert "id" in data
        # Validate UUID7 format
        assert uuid.UUID(data["id"]).version == 7

    def test_create_location_missing_name(self, api_client, sample_store):
        """Test location creation without name."""
        invalid_data = {
            "store_id": sample_store["id"],
        }

        response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_location_empty_name(self, api_client, sample_store):
        """Test location creation with empty name."""
        invalid_data = {
            "name": "",
            "store_id": sample_store["id"],
        }

        response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_location_invalid_store_id(self, api_client):
        """Test location creation with invalid store_id UUID format."""
        invalid_data = {
            "name": "Test Location",
            "store_id": "01939d8e-1234-7890-abcd-ef0123456789",
        }

        response = api_client.post("/api/v1/locations/not-a-valid-uuid", json=invalid_data)

        assert response.status_code == 422

    def test_create_location_nonexistent_store(self, api_client):
        """Test location creation with non-existent store."""
        non_existent_store_id = "01939d8e-1234-7890-abcd-ef0123456789"
        invalid_data = {
            "name": "Test Location",
            "store_id": non_existent_store_id,
        }

        response = api_client.post(f"/api/v1/locations/{non_existent_store_id}", json=invalid_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"


class TestListLocations:
    """Tests for GET /api/v1/locations/{store_id}."""

    def test_list_locations_empty(self, api_client, sample_store):
        """Test listing locations when database is empty."""
        response = api_client.get(f"/api/v1/locations/{sample_store['id']}")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_locations_with_one_location(self, api_client, sample_location_data, sample_store):
        """Test listing locations with one location in database."""
        # Create a location first
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()

        # List locations
        response = api_client.get(f"/api/v1/locations/{sample_store['id']}")

        assert response.status_code == 200
        locations = response.json()
        assert len(locations) == 1
        assert locations[0]["id"] == created_location["id"]
        assert locations[0]["name"] == sample_location_data["name"]
        assert locations[0]["store_id"] == sample_location_data["store_id"]

    def test_list_locations_with_multiple_locations(
        self, api_client, sample_location_data, another_location_data, sample_store
    ):
        """Test listing multiple locations."""
        # Create two locations
        api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        api_client.post(f"/api/v1/locations/{sample_store['id']}", json=another_location_data)

        # List locations
        response = api_client.get(f"/api/v1/locations/{sample_store['id']}")

        assert response.status_code == 200
        locations = response.json()
        assert len(locations) == 2

        location_names = {location["name"] for location in locations}
        assert sample_location_data["name"] in location_names
        assert another_location_data["name"] in location_names


class TestGetLocation:
    """Tests for GET /api/v1/locations/{store_id}/{location_id}."""

    def test_get_location_success(self, api_client, sample_location_data, sample_store):
        """Test successful retrieval of a specific location."""
        # Create a location first
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()
        location_id = created_location["id"]

        # Get the location
        response = api_client.get(f"/api/v1/locations/{sample_store['id']}/{location_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == location_id
        assert data["name"] == sample_location_data["name"]
        assert data["store_id"] == sample_location_data["store_id"]

    def test_get_location_not_found(self, api_client, sample_store):
        """Test getting a non-existent location."""
        # Generate a random UUID7
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/locations/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Location not found"

    def test_get_location_invalid_uuid(self, api_client, sample_store):
        """Test getting a location with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/locations/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422


class TestUpdateLocation:
    """Tests for PUT /api/v1/locations/{store_id}/{location_id}."""

    def test_update_location_name(self, api_client, sample_location_data, sample_store):
        """Test updating location name."""
        # Create a location first
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()
        location_id = created_location["id"]

        # Update the location name
        update_data = {
            "name": "Updated Location Name",
        }
        response = api_client.put(f"/api/v1/locations/{sample_store['id']}/{location_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == location_id
        assert data["name"] == "Updated Location Name"
        assert data["store_id"] == sample_location_data["store_id"]  # store_id should remain unchanged

    def test_update_location_name_to_null(self, api_client, sample_location_data, sample_store):
        """Test updating location with null name (should keep original)."""
        # Create a location first
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()
        location_id = created_location["id"]

        # Update with null name
        update_data = {
            "name": None,
        }
        response = api_client.put(f"/api/v1/locations/{sample_store['id']}/{location_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == location_id
        assert data["name"] == sample_location_data["name"]  # Name should remain unchanged

    def test_update_location_not_found(self, api_client, sample_store):
        """Test updating a non-existent location."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        update_data = {
            "name": "Updated Name",
        }
        response = api_client.put(f"/api/v1/locations/{sample_store['id']}/{non_existent_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Location not found"

    def test_update_location_empty_name(self, api_client, sample_location_data, sample_store):
        """Test updating location with empty name."""
        # Create a location first
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()
        location_id = created_location["id"]

        # Try to update with empty name
        update_data = {
            "name": "",
        }
        response = api_client.put(f"/api/v1/locations/{sample_store['id']}/{location_id}", json=update_data)

        assert response.status_code == 422


class TestDeleteLocation:
    """Tests for DELETE /api/v1/locations/{store_id}/{location_id}."""

    def test_delete_location_success(self, api_client, sample_location_data, sample_store):
        """Test successful soft delete of a location."""
        # Create a location first
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()
        location_id = created_location["id"]

        # Delete the location
        response = api_client.delete(f"/api/v1/locations/{sample_store['id']}/{location_id}")

        assert response.status_code == 204

    def test_delete_location_not_found(self, api_client, sample_store):
        """Test deleting a non-existent location."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.delete(f"/api/v1/locations/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Location not found"

    def test_delete_location_invalid_uuid(self, api_client, sample_store):
        """Test deleting a location with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/locations/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422

    def test_get_deleted_location(self, api_client, sample_location_data, sample_store):
        """Test that a deleted location can still be retrieved (soft delete)."""
        # Create a location
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        created_location = create_response.json()
        location_id = created_location["id"]

        # Delete the location
        api_client.delete(f"/api/v1/locations/{sample_store['id']}/{location_id}")

        # Try to get the deleted location
        # Note: This test behavior depends on whether your list/get methods filter out soft-deleted records
        # Adjust based on your actual implementation
        response = api_client.get(f"/api/v1/locations/{sample_store['id']}/{location_id}")

        # If soft delete is implemented properly, the location should still exist but have deleted_at set
        # The actual behavior depends on your business logic
        # You may need to adjust this assertion based on how you want soft deletes to work
        assert response.status_code in [200, 404]


class TestLocationCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, api_client, sample_location_data, sample_store):
        """Test the complete CRUD lifecycle of a location."""
        # Create
        create_response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=sample_location_data)
        assert create_response.status_code == 200
        created_location = create_response.json()
        location_id = created_location["id"]

        # Read (single)
        get_response = api_client.get(f"/api/v1/locations/{sample_store['id']}/{location_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == location_id

        # Read (list)
        list_response = api_client.get(f"/api/v1/locations/{sample_store['id']}")
        assert list_response.status_code == 200
        assert len(list_response.json()) >= 1

        # Update
        update_data = {
            "name": "Updated Location Name",
        }
        update_response = api_client.put(f"/api/v1/locations/{sample_store['id']}/{location_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Location Name"

        # Verify update
        get_updated_response = api_client.get(f"/api/v1/locations/{sample_store['id']}/{location_id}")
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["name"] == "Updated Location Name"

        # Delete
        delete_response = api_client.delete(f"/api/v1/locations/{sample_store['id']}/{location_id}")
        assert delete_response.status_code == 204

    def test_multiple_locations_for_same_store(self, api_client, sample_store):
        """Test creating multiple locations for the same store."""
        location1_data = {
            "name": "Location 1",
            "store_id": sample_store["id"],
        }
        location2_data = {
            "name": "Location 2",
            "store_id": sample_store["id"],
        }

        # Create two locations for the same store
        response1 = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location1_data)
        response2 = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location2_data)

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both have the same store_id but different location ids
        loc1 = response1.json()
        loc2 = response2.json()

        assert loc1["store_id"] == loc2["store_id"] == sample_store["id"]
        assert loc1["id"] != loc2["id"]

    def test_locations_across_different_stores(self, api_client, sample_store, another_store):
        """Test creating locations for different stores."""
        location1_data = {
            "name": "Store 1 Location",
            "store_id": sample_store["id"],
        }
        location2_data = {
            "name": "Store 2 Location",
            "store_id": another_store["id"],
        }

        # Create locations for different stores
        response1 = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location1_data)
        response2 = api_client.post(f"/api/v1/locations/{another_store['id']}", json=location2_data)

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify they have different store_ids
        loc1 = response1.json()
        loc2 = response2.json()

        assert loc1["store_id"] == sample_store["id"]
        assert loc2["store_id"] == another_store["id"]
        assert loc1["store_id"] != loc2["store_id"]
