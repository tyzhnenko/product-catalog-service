# ruff: noqa: S101, D100, D101, D102, D103
import uuid

import pytest


@pytest.fixture
def sample_store(api_client):
    """Create a sample store for testing bundles."""
    store_data = {
        "name": "Test Store for Bundles",
        "url": "https://teststorebundles.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def another_store(api_client):
    """Create another store for testing bundles."""
    store_data = {
        "name": "Another Bundle Store",
        "url": "https://anotherbundlestore.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def sample_category(api_client, sample_store):
    """Create a sample category for testing bundles."""
    category_data = {
        "name": "Bundle Deals",
        "description": "Special bundle offers",
        "status": "active",
        "path": "/bundle-deals",
    }
    response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def another_category(api_client, sample_store):
    """Create another category for testing bundles."""
    category_data = {
        "name": "Coffee Sets",
        "description": "Coffee bundle sets",
        "status": "active",
        "path": "/coffee-sets",
    }
    response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def sample_product(api_client, sample_store):
    """Create a sample product for testing bundle variants."""
    product_data = {
        "name": "Ethiopian Coffee",
        "tags": [],
        "categories": [],
    }
    response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def another_product(api_client, sample_store):
    """Create another product for testing bundle variants."""
    product_data = {
        "name": "Colombian Coffee",
        "tags": [],
        "categories": [],
    }
    response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def sample_variant(api_client, sample_store, sample_product):
    """Create a sample variant for testing bundle components."""
    variant_data = {
        "title": "250g Bag",
        "sku": "ETH-250",
        "options": [{"name": "size", "value": "250g"}],
    }
    response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=variant_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def another_variant(api_client, sample_store, another_product):
    """Create another variant for testing bundle components."""
    variant_data = {
        "title": "500g Bag",
        "sku": "COL-500",
        "options": [{"name": "size", "value": "500g"}],
    }
    response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}", json=variant_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def sample_bundle_data(sample_category, sample_variant, another_variant):
    """Sample data for creating a bundle."""
    return {
        "name": "Coffee Lover's Bundle",
        "description": "A perfect combination of Ethiopian and Colombian coffee",
        "components": [sample_variant["id"], another_variant["id"]],
        "categories": [sample_category["id"]],
        "attributes": {
            "discount": {"type": "string", "name": "discount", "value": "20%"},
            "savings": {"type": "string", "name": "savings", "value": "10 USD"},
        },
        "price": {
            "USD": {"type": "decimal", "name": "USD Price", "value": "45.99"},
            "EUR": {"type": "decimal", "name": "EUR Price", "value": "42.50"},
        },
    }


@pytest.fixture
def another_bundle_data(another_category):
    """Another sample bundle data for testing multiple bundles."""
    return {
        "name": "Starter Kit",
        "description": "Everything you need to start your coffee journey",
        "categories": [another_category["id"]],
        "price": {
            "USD": {"type": "decimal", "name": "USD Price", "value": "29.99"},
        },
    }


@pytest.fixture
def minimal_bundle_data():
    """Minimal bundle data with only required fields."""
    return {
        "name": "Simple Bundle",
    }


class TestCreateBundle:
    """Tests for POST /api/v1/bundles/{store_id}."""

    def test_create_bundle_success(self, api_client, sample_bundle_data, sample_store):
        """Test successful bundle creation."""
        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == sample_bundle_data["name"]
        assert data["description"] == sample_bundle_data["description"]
        assert len(data["components"]) == 2
        assert data["categories"] == sample_bundle_data["categories"]
        assert "discount" in data["attributes"]
        assert data["attributes"]["discount"]["value"] == "20%"
        assert "USD" in data["price"]
        assert data["price"]["USD"]["value"] == "45.99"
        assert "id" in data
        # Validate UUID7 format
        assert uuid.UUID(data["id"]).version == 7

    def test_create_bundle_minimal_fields(self, api_client, minimal_bundle_data, sample_store):
        """Test bundle creation with minimal required fields."""
        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=minimal_bundle_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == minimal_bundle_data["name"]
        assert data["description"] is None
        assert data["components"] is None
        assert data["categories"] is None
        assert "id" in data

    def test_create_bundle_missing_name(self, api_client, sample_store):
        """Test bundle creation without name."""
        invalid_data = {}

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_bundle_empty_name(self, api_client, sample_store):
        """Test bundle creation with empty name."""
        invalid_data = {
            "name": "",
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_bundle_invalid_store_id(self, api_client, sample_bundle_data):
        """Test bundle creation with invalid store_id UUID format."""
        response = api_client.post("/api/v1/bundles/not-a-valid-uuid", json=sample_bundle_data)

        assert response.status_code == 422

    def test_create_bundle_nonexistent_store(self, api_client, sample_bundle_data):
        """Test bundle creation with non-existent store."""
        non_existent_store_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.post(f"/api/v1/bundles/{non_existent_store_id}", json=sample_bundle_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_create_bundle_name_too_long(self, api_client, sample_store):
        """Test bundle creation with name exceeding max length."""
        invalid_data = {
            "name": "A" * 257,  # Max is 256
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_bundle_with_invalid_category(self, api_client, sample_store):
        """Test bundle creation with non-existent category - should filter it out."""
        invalid_data = {
            "name": "Test Bundle",
            "categories": ["01939d8e-1234-7890-abcd-ef0123456789"],  # Non-existent category
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid category should be filtered out
        assert data["categories"] == []

    def test_create_bundle_with_category_from_different_store(self, api_client, sample_store, another_store):
        """Test bundle creation with category from a different store - should filter it out."""
        # Create category in another store
        category_data = {
            "name": "Other Store Category",
            "description": "Category in different store",
            "status": "active",
            "path": "/other",
        }
        category_response = api_client.post(f"/api/v1/categories/{another_store['id']}", json=category_data)
        category = category_response.json()

        # Try to create bundle in sample_store with category from another_store
        invalid_data = {
            "name": "Test Bundle",
            "categories": [category["id"]],
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 200
        data = response.json()
        # Category from different store should be filtered out
        assert data["categories"] == []

    def test_create_bundle_with_invalid_component(self, api_client, sample_store):
        """Test bundle creation with non-existent component - should filter it out."""
        invalid_data = {
            "name": "Test Bundle",
            "components": ["01939d8e-1234-7890-abcd-ef0123456789"],  # Non-existent variant
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid component should be filtered out
        assert data["components"] == []

    def test_create_bundle_with_component_from_different_store(self, api_client, sample_store, another_store):
        """Test bundle creation with component from a different store - should filter it out."""
        # Create product in another store
        product_data = {
            "name": "Other Store Product",
            "tags": [],
            "categories": [],
        }
        product_response = api_client.post(f"/api/v1/products/{another_store['id']}", json=product_data)
        product = product_response.json()

        # Create variant in another store
        variant_data = {
            "title": "Other Store Variant",
            "sku": "OTHER-001",
            "options": [],
        }
        variant_response = api_client.post(f"/api/v1/variants/{another_store['id']}/{product['id']}", json=variant_data)
        variant = variant_response.json()

        # Try to create bundle in sample_store with variant from another_store
        invalid_data = {
            "name": "Test Bundle",
            "components": [variant["id"]],
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 200
        data = response.json()
        # Component from different store should be filtered out
        assert data["components"] == []

    def test_create_bundle_with_multiple_categories(self, api_client, sample_store, sample_category, another_category):
        """Test bundle creation with multiple categories."""
        bundle_data = {
            "name": "Multi-Category Bundle",
            "categories": [sample_category["id"], another_category["id"]],
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 2
        assert sample_category["id"] in data["categories"]
        assert another_category["id"] in data["categories"]

    def test_create_bundle_with_multiple_components(self, api_client, sample_store, sample_variant, another_variant):
        """Test bundle creation with multiple components."""
        bundle_data = {
            "name": "Multi-Component Bundle",
            "components": [sample_variant["id"], another_variant["id"]],
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["components"]) == 2
        assert sample_variant["id"] in data["components"]
        assert another_variant["id"] in data["components"]

    def test_create_bundle_with_mixed_valid_invalid_categories(self, api_client, sample_store, sample_category):
        """Test bundle creation with mix of valid and invalid categories - keeps only valid ones."""
        bundle_data = {
            "name": "Mixed Categories Bundle",
            "categories": [
                sample_category["id"],
                "01939d8e-1234-7890-abcd-ef0123456789",  # Invalid
                "01939d8e-5678-7890-abcd-ef0123456789",  # Invalid
            ],
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        # Only the valid category should be kept
        assert len(data["categories"]) == 1
        assert data["categories"][0] == sample_category["id"]

    def test_create_bundle_with_mixed_valid_invalid_components(self, api_client, sample_store, sample_variant):
        """Test bundle creation with mix of valid and invalid components - keeps only valid ones."""
        bundle_data = {
            "name": "Mixed Components Bundle",
            "components": [
                sample_variant["id"],
                "01939d8e-1234-7890-abcd-ef0123456789",  # Invalid
                "01939d8e-5678-7890-abcd-ef0123456789",  # Invalid
            ],
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        # Only the valid component should be kept
        assert len(data["components"]) == 1
        assert data["components"][0] == sample_variant["id"]


class TestListBundles:
    """Tests for GET /api/v1/bundles/{store_id}."""

    def test_list_bundles_empty(self, api_client, sample_store):
        """Test listing bundles when database is empty."""
        response = api_client.get(f"/api/v1/bundles/{sample_store['id']}")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_bundles_with_one_bundle(self, api_client, sample_bundle_data, sample_store):
        """Test listing bundles with one bundle in database."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        created_bundle = create_response.json()

        # List bundles
        response = api_client.get(f"/api/v1/bundles/{sample_store['id']}")

        assert response.status_code == 200
        bundles = response.json()
        assert len(bundles) == 1
        assert bundles[0]["id"] == created_bundle["id"]
        assert bundles[0]["name"] == sample_bundle_data["name"]

    def test_list_bundles_with_multiple_bundles(
        self, api_client, sample_bundle_data, another_bundle_data, sample_store
    ):
        """Test listing multiple bundles."""
        # Create two bundles
        api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=another_bundle_data)

        # List bundles
        response = api_client.get(f"/api/v1/bundles/{sample_store['id']}")

        assert response.status_code == 200
        bundles = response.json()
        assert len(bundles) == 2

        bundle_names = {bundle["name"] for bundle in bundles}
        assert sample_bundle_data["name"] in bundle_names
        assert another_bundle_data["name"] in bundle_names

    def test_list_bundles_different_stores(self, api_client, sample_bundle_data, sample_store, another_store):
        """Test that bundles from different stores are isolated."""
        # Create bundle in first store
        api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)

        # List bundles from second store
        response = api_client.get(f"/api/v1/bundles/{another_store['id']}")

        assert response.status_code == 200
        bundles = response.json()
        assert len(bundles) == 0

    def test_list_bundles_nonexistent_store(self, api_client):
        """Test listing bundles for non-existent store."""
        non_existent_store_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/bundles/{non_existent_store_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"


class TestGetBundle:
    """Tests for GET /api/v1/bundles/{store_id}/{bundle_id}."""

    def test_get_bundle_success(self, api_client, sample_bundle_data, sample_store):
        """Test successful retrieval of a specific bundle."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        created_bundle = create_response.json()
        bundle_id = created_bundle["id"]

        # Get the bundle
        response = api_client.get(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert data["name"] == sample_bundle_data["name"]
        assert data["description"] == sample_bundle_data["description"]

    def test_get_bundle_not_found(self, api_client, sample_store):
        """Test getting a non-existent bundle."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/bundles/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Bundle not found"

    def test_get_bundle_wrong_store(self, api_client, sample_bundle_data, sample_store, another_store):
        """Test getting a bundle from wrong store."""
        # Create bundle in first store
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Try to get from second store
        response = api_client.get(f"/api/v1/bundles/{another_store['id']}/{bundle_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Bundle not found"

    def test_get_bundle_invalid_uuid(self, api_client, sample_store):
        """Test getting a bundle with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/bundles/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422


class TestUpdateBundle:
    """Tests for PATCH /api/v1/bundles/{store_id}/{bundle_id}."""

    def test_update_bundle_name(self, api_client, sample_bundle_data, sample_store):
        """Test updating bundle name."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update the bundle name
        update_data = {"name": "Updated Bundle Name"}
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert data["name"] == "Updated Bundle Name"
        assert data["description"] == sample_bundle_data["description"]  # Should remain unchanged

    def test_update_bundle_description(self, api_client, sample_bundle_data, sample_store):
        """Test updating bundle description."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update the bundle description
        update_data = {"description": "New bundle description"}
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert data["description"] == "New bundle description"
        assert data["name"] == sample_bundle_data["name"]  # Should remain unchanged

    def test_update_bundle_components(self, api_client, sample_bundle_data, sample_store, sample_variant):
        """Test updating bundle components."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update the bundle components
        update_data = {"components": [sample_variant["id"]]}
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert len(data["components"]) == 1
        assert data["components"][0] == sample_variant["id"]

    def test_update_bundle_categories(self, api_client, sample_bundle_data, sample_store, another_category):
        """Test updating bundle categories."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update the bundle categories
        update_data = {"categories": [another_category["id"]]}
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert len(data["categories"]) == 1
        assert data["categories"][0] == another_category["id"]

    def test_update_bundle_price(self, api_client, sample_bundle_data, sample_store):
        """Test updating bundle price."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update the bundle price
        update_data = {
            "price": {
                "USD": {"type": "decimal", "name": "USD Price", "value": "99.99"},
                "EUR": {"type": "decimal", "name": "EUR Price", "value": "89.99"},
            }
        }
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert data["price"]["USD"]["value"] == "99.99"
        assert data["price"]["EUR"]["value"] == "89.99"

    def test_update_bundle_attributes(self, api_client, sample_bundle_data, sample_store):
        """Test updating bundle attributes."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update the bundle attributes
        update_data = {
            "attributes": {
                "new_attr": {"type": "string", "name": "new_attr", "value": "new value"},
                "feature": {"type": "string", "name": "feature", "value": "premium"},
            }
        }
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert data["attributes"]["new_attr"]["value"] == "new value"
        assert data["attributes"]["feature"]["value"] == "premium"

    def test_update_bundle_multiple_fields(self, api_client, sample_bundle_data, sample_store):
        """Test updating multiple bundle fields at once."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update multiple fields
        update_data = {
            "name": "Completely Updated Bundle",
            "description": "Completely new description",
            "price": {
                "USD": {"type": "decimal", "name": "USD Price", "value": "199.99"},
            },
        }
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bundle_id
        assert data["name"] == "Completely Updated Bundle"
        assert data["description"] == "Completely new description"
        assert data["price"]["USD"]["value"] == "199.99"

    def test_update_bundle_not_found(self, api_client, sample_store):
        """Test updating a non-existent bundle."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"
        update_data = {"name": "Updated Name"}

        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{non_existent_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Bundle not found"

    def test_update_bundle_wrong_store(self, api_client, sample_bundle_data, sample_store, another_store):
        """Test updating a bundle from wrong store."""
        # Create bundle in first store
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Try to update from second store
        update_data = {"name": "Hacked Name"}
        response = api_client.patch(f"/api/v1/bundles/{another_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Bundle not found"

    def test_update_bundle_with_invalid_category(self, api_client, sample_bundle_data, sample_store):
        """Test updating bundle with non-existent category - should filter it out."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update with invalid category
        update_data = {"categories": ["01939d8e-1234-7890-abcd-ef0123456789"]}
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid category should be filtered out
        assert data["categories"] == []

    def test_update_bundle_with_invalid_component(self, api_client, sample_bundle_data, sample_store):
        """Test updating bundle with non-existent component - should filter it out."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update with invalid component
        update_data = {"components": ["01939d8e-1234-7890-abcd-ef0123456789"]}
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid component should be filtered out
        assert data["components"] == []


class TestDeleteBundle:
    """Tests for DELETE /api/v1/bundles/{store_id}/{bundle_id}."""

    def test_delete_bundle_success(self, api_client, sample_bundle_data, sample_store):
        """Test successful bundle deletion."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Delete the bundle
        response = api_client.delete(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}")

        assert response.status_code == 204

        # Verify bundle is not in list anymore
        list_response = api_client.get(f"/api/v1/bundles/{sample_store['id']}")
        bundles = list_response.json()
        assert len(bundles) == 0

    def test_delete_bundle_not_found(self, api_client, sample_store):
        """Test deleting a non-existent bundle."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.delete(f"/api/v1/bundles/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Bundle not found"

    def test_delete_bundle_wrong_store(self, api_client, sample_bundle_data, sample_store, another_store):
        """Test deleting a bundle from wrong store."""
        # Create bundle in first store
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Try to delete from second store
        response = api_client.delete(f"/api/v1/bundles/{another_store['id']}/{bundle_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Bundle not found"

        # Verify bundle still exists in first store
        get_response = api_client.get(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}")
        assert get_response.status_code == 200

    def test_delete_bundle_invalid_uuid(self, api_client, sample_store):
        """Test deleting a bundle with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/bundles/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422

    def test_delete_bundle_twice(self, api_client, sample_bundle_data, sample_store):
        """Test that deleting the same bundle twice returns 404."""
        # Create a bundle first
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=sample_bundle_data)
        bundle_id = create_response.json()["id"]

        # Delete the bundle first time
        first_delete = api_client.delete(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}")
        assert first_delete.status_code == 204

        # Try to delete again
        second_delete = api_client.delete(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}")
        assert second_delete.status_code == 404
        assert second_delete.json()["detail"] == "Bundle not found"


class TestBundleLocationPrice:
    """Tests for location_price sanitization in bundles."""

    @pytest.fixture
    def sample_location(self, api_client, sample_store):
        """Create a sample location for testing."""
        location_data = {
            "name": "Downtown Store",
            "attributes": {
                "address": {"type": "string", "name": "address", "value": "123 Main St"},
            },
        }
        response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location_data)
        assert response.status_code == 200
        return response.json()

    @pytest.fixture
    def another_location(self, api_client, sample_store):
        """Create another location for testing."""
        location_data = {
            "name": "Airport Store",
            "attributes": {
                "address": {"type": "string", "name": "address", "value": "456 Airport Rd"},
            },
        }
        response = api_client.post(f"/api/v1/locations/{sample_store['id']}", json=location_data)
        assert response.status_code == 200
        return response.json()

    def test_create_bundle_with_location_price(self, api_client, sample_store, sample_location):
        """Test creating a bundle with location-specific pricing."""
        bundle_data = {
            "name": "Location-Priced Bundle",
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "49.99"}}
            },
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"] is not None
        assert sample_location["id"] in data["location_price"]

    def test_create_bundle_filters_invalid_location_ids(self, api_client, sample_store, sample_location):
        """Test that invalid location IDs are filtered out."""
        bundle_data = {
            "name": "Mixed Locations Bundle",
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "49.99"}},
                "01939d8e-1234-7890-abcd-ef0123456789": {  # Invalid location
                    "retail": {"type": "decimal", "name": "Retail Price", "value": "59.99"}
                },
            },
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"] is not None
        assert sample_location["id"] in data["location_price"]
        assert "01939d8e-1234-7890-abcd-ef0123456789" not in data["location_price"]

    def test_create_bundle_all_invalid_locations_becomes_none(self, api_client, sample_store):
        """Test that when all locations are invalid, location_price becomes None."""
        bundle_data = {
            "name": "Invalid Locations Bundle",
            "location_price": {
                "01939d8e-1234-7890-abcd-ef0123456789": {
                    "retail": {"type": "decimal", "name": "Retail Price", "value": "49.99"}
                },
            },
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"] is None

    def test_create_bundle_location_from_different_store_filtered(self, api_client, sample_store, another_store):
        """Test that locations from a different store are filtered out."""
        # Create location in another store
        location_data = {
            "name": "Other Store Location",
            "attributes": {},
        }
        location_response = api_client.post(f"/api/v1/locations/{another_store['id']}", json=location_data)
        other_location = location_response.json()

        # Try to create bundle in sample_store with location from another_store
        bundle_data = {
            "name": "Cross-Store Location Bundle",
            "location_price": {
                other_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "49.99"}},
            },
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        # Location from different store should be filtered out
        assert data["location_price"] is None

    def test_update_bundle_with_location_price(self, api_client, sample_store, minimal_bundle_data, sample_location):
        """Test updating a bundle to add location prices."""
        # Create bundle without location prices
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=minimal_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update with location prices
        update_data = {
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "39.99"}}
            }
        }
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"] is not None
        assert sample_location["id"] in data["location_price"]

    def test_update_bundle_filters_invalid_location_ids(
        self, api_client, sample_store, minimal_bundle_data, sample_location
    ):
        """Test that updating with invalid location IDs filters them out."""
        # Create bundle
        create_response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=minimal_bundle_data)
        bundle_id = create_response.json()["id"]

        # Update with mixed valid/invalid locations
        update_data = {
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "39.99"}},
                "01939d8e-1234-7890-abcd-ef0123456789": {
                    "retail": {"type": "decimal", "name": "Retail Price", "value": "49.99"}
                },
            }
        }
        response = api_client.patch(f"/api/v1/bundles/{sample_store['id']}/{bundle_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["location_price"] is not None
        assert sample_location["id"] in data["location_price"]
        assert "01939d8e-1234-7890-abcd-ef0123456789" not in data["location_price"]

    def test_create_bundle_with_multiple_location_prices(
        self, api_client, sample_store, sample_location, another_location
    ):
        """Test creating a bundle with multiple location-specific prices."""
        bundle_data = {
            "name": "Multi-Location Bundle",
            "location_price": {
                sample_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "49.99"}},
                another_location["id"]: {"retail": {"type": "decimal", "name": "Retail Price", "value": "54.99"}},
            },
        }

        response = api_client.post(f"/api/v1/bundles/{sample_store['id']}", json=bundle_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["location_price"]) == 2
        assert sample_location["id"] in data["location_price"]
        assert another_location["id"] in data["location_price"]
