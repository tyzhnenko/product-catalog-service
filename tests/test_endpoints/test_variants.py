# ruff: noqa: S101, D100, D101, D102, D103
import uuid

import pytest


@pytest.fixture
def sample_store(api_client):
    """Create a sample store for testing variants."""
    store_data = {
        "name": "Test Store for Variants",
        "url": "https://teststorevariants.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def another_store(api_client):
    """Create another store for testing variants."""
    store_data = {
        "name": "Another Variant Store",
        "url": "https://anothervariantstore.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def sample_product(api_client, sample_store):
    """Create a sample product for testing variants."""
    product_data = {
        "name": "Ethiopian Coffee",
        "description": "Premium Ethiopian coffee beans",
        "tags": ["single-origin"],
    }
    response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
    return response.json()


@pytest.fixture
def another_product(api_client, sample_store):
    """Create another product for testing variants."""
    product_data = {
        "name": "Colombian Coffee",
        "description": "Colombian coffee beans",
        "tags": ["single-origin"],
    }
    response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
    return response.json()


@pytest.fixture
def sample_variant_data():
    """Sample data for creating a variant."""
    return {
        "title": "250g Whole Beans",
        "sku": "ETH-250-WB",
        "upc": "123456789012",
        "ean": "1234567890123",
        "options": [
            {"name": "Size", "value": "250g"},
            {"name": "Grind", "value": "Whole Beans"},
        ],
        "attributes": [
            {"type": "string", "name": "origin", "value": "Yirgacheffe"},
            {"type": "integer", "name": "altitude", "value": 1800},
        ],
    }


@pytest.fixture
def another_variant_data():
    """Another sample variant data for testing multiple variants."""
    return {
        "title": "500g Ground",
        "sku": "ETH-500-GR",
        "options": [
            {"name": "Size", "value": "500g"},
            {"name": "Grind", "value": "Ground"},
        ],
    }


@pytest.fixture
def minimal_variant_data():
    """Minimal variant data with only required fields."""
    return {
        "title": "Simple Variant",
        "options": [],
    }


class TestCreateVariant:
    """Tests for POST /api/v1/variants/{store_id}/{product_id}."""

    def test_create_variant_success(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test successful variant creation."""
        response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == sample_variant_data["title"]
        assert data["sku"] == sample_variant_data["sku"]
        assert data["product_id"] == sample_product["id"]
        assert len(data["options"]) == 2
        assert len(data["attributes"]) == 2
        assert "id" in data
        # Validate UUID7 format
        assert uuid.UUID(data["id"]).version == 7

    def test_create_variant_minimal_fields(self, api_client, minimal_variant_data, sample_store, sample_product):
        """Test variant creation with minimal required fields."""
        response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=minimal_variant_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == minimal_variant_data["title"]
        assert data["options"] == []
        assert "id" in data

    def test_create_variant_missing_title(self, api_client, sample_store, sample_product):
        """Test variant creation without title."""
        invalid_data = {
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_variant_empty_title(self, api_client, sample_store, sample_product):
        """Test variant creation with empty title."""
        invalid_data = {
            "title": "",
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_variant_invalid_store_id(self, api_client, sample_variant_data, sample_product):
        """Test variant creation with invalid store_id UUID format."""
        response = api_client.post(
            f"/api/v1/variants/not-a-valid-uuid/{sample_product['id']}", json=sample_variant_data
        )

        assert response.status_code == 422

    def test_create_variant_nonexistent_store(self, api_client, sample_variant_data, sample_product):
        """Test variant creation with non-existent store."""
        non_existent_store_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.post(
            f"/api/v1/variants/{non_existent_store_id}/{sample_product['id']}", json=sample_variant_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Product or store not found"

    def test_create_variant_nonexistent_product(self, api_client, sample_variant_data, sample_store):
        """Test variant creation with non-existent product."""
        non_existent_product_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{non_existent_product_id}", json=sample_variant_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Product or store not found"

    def test_create_variant_title_too_long(self, api_client, sample_store, sample_product):
        """Test variant creation with title exceeding max length."""
        invalid_data = {
            "title": "A" * 257,  # Max is 256
            "options": [],
        }

        response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=invalid_data)

        assert response.status_code == 422


class TestListVariants:
    """Tests for GET /api/v1/variants/{store_id}/{product_id}."""

    def test_list_variants_empty(self, api_client, sample_store, sample_product):
        """Test listing variants when database is empty."""
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_variants_with_one_variant(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test listing variants with one variant in database."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        created_variant = create_response.json()

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        variants = response.json()
        assert len(variants) == 1
        assert variants[0]["id"] == created_variant["id"]
        assert variants[0]["title"] == sample_variant_data["title"]

    def test_list_variants_with_multiple_variants(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Test listing multiple variants."""
        # Create two variants
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data)

        # List variants
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")

        assert response.status_code == 200
        variants = response.json()
        assert len(variants) == 2

        variant_titles = {variant["title"] for variant in variants}
        assert sample_variant_data["title"] in variant_titles
        assert another_variant_data["title"] in variant_titles

    def test_list_variants_different_products(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test that variants from different products are isolated."""
        # Create variant for first product
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data)

        # List variants for second product
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}")

        assert response.status_code == 200
        variants = response.json()
        assert len(variants) == 0

    def test_list_variants_nonexistent_product(self, api_client, sample_store):
        """Test listing variants for non-existent product."""
        non_existent_product_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{non_existent_product_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Product or store not found"


class TestGetVariant:
    """Tests for GET /api/v1/variants/{store_id}/{product_id}/{variant_id}."""

    def test_get_variant_success(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test successful retrieval of a specific variant."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        created_variant = create_response.json()
        variant_id = created_variant["id"]

        # Get the variant
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == variant_id
        assert data["title"] == sample_variant_data["title"]
        assert data["sku"] == sample_variant_data["sku"]

    def test_get_variant_not_found(self, api_client, sample_store, sample_product):
        """Test getting a non-existent variant."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_get_variant_wrong_product(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test getting a variant from wrong product."""
        # Create variant for first product
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Try to get from second product
        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}/{variant_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_get_variant_invalid_uuid(self, api_client, sample_store, sample_product):
        """Test getting a variant with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{invalid_id}")

        assert response.status_code == 422


class TestUpdateVariant:
    """Tests for PUT /api/v1/variants/{store_id}/{product_id}/{variant_id}."""

    def test_update_variant_title(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant title."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update the variant title
        update_data = {"title": "Updated Variant Title"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == variant_id
        assert data["title"] == "Updated Variant Title"
        assert data["sku"] == sample_variant_data["sku"]  # Should remain unchanged

    def test_update_variant_sku(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant SKU."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update the SKU
        update_data = {"sku": "NEW-SKU-123"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sku"] == "NEW-SKU-123"

    def test_update_variant_options(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant options."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update options
        update_data = {"options": [{"name": "Weight", "value": "1kg"}]}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["options"]) == 1
        assert data["options"][0]["name"] == "Weight"

    def test_update_variant_attributes(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test updating variant attributes."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Update attributes
        update_data = {"attributes": [{"type": "string", "name": "color", "value": "brown"}]}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["attributes"]) == 1
        assert data["attributes"][0]["name"] == "color"

    def test_update_variant_not_found(self, api_client, sample_store, sample_product):
        """Test updating a non-existent variant."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        update_data = {"title": "Updated Title"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{non_existent_id}", json=update_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_update_variant_wrong_product(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test updating a variant from wrong product."""
        # Create variant for first product
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Try to update from second product
        update_data = {"title": "Hacked Title"}
        response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{another_product['id']}/{variant_id}", json=update_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"


class TestDeleteVariant:
    """Tests for DELETE /api/v1/variants/{store_id}/{product_id}/{variant_id}."""

    def test_delete_variant_success(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test successful soft delete of a variant."""
        # Create a variant first
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Delete the variant
        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")

        assert response.status_code == 204

    def test_delete_variant_not_found(self, api_client, sample_store, sample_product):
        """Test deleting a non-existent variant."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_delete_variant_wrong_product(
        self, api_client, sample_variant_data, sample_store, sample_product, another_product
    ):
        """Test deleting a variant from wrong product."""
        # Create variant for first product
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        variant_id = create_response.json()["id"]

        # Try to delete from second product
        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{another_product['id']}/{variant_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Variant not found"

    def test_delete_variant_invalid_uuid(self, api_client, sample_store, sample_product):
        """Test deleting a variant with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{invalid_id}")

        assert response.status_code == 422


class TestVariantCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, api_client, sample_variant_data, sample_store, sample_product):
        """Test the complete CRUD lifecycle of a variant."""
        # Create
        create_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert create_response.status_code == 200
        created_variant = create_response.json()
        variant_id = created_variant["id"]

        # Read (single)
        get_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == variant_id

        # Read (list)
        list_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")
        assert list_response.status_code == 200
        assert len(list_response.json()) >= 1

        # Update
        update_data = {
            "title": "Updated Variant Title",
            "sku": "UPDATED-SKU",
        }
        update_response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}", json=update_data
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Variant Title"
        assert update_response.json()["sku"] == "UPDATED-SKU"

        # Verify update
        get_updated_response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}"
        )
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["title"] == "Updated Variant Title"

        # Delete
        delete_response = api_client.delete(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}"
        )
        assert delete_response.status_code == 204

        # Verify deletion
        get_deleted_response = api_client.get(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant_id}"
        )
        assert get_deleted_response.status_code == 404

    def test_multiple_variants_for_product(
        self, api_client, sample_variant_data, another_variant_data, sample_store, sample_product
    ):
        """Test creating and managing multiple variants for the same product."""
        # Create first variant
        variant1_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=sample_variant_data
        )
        assert variant1_response.status_code == 200
        variant1_id = variant1_response.json()["id"]

        # Create second variant
        variant2_response = api_client.post(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}", json=another_variant_data
        )
        assert variant2_response.status_code == 200
        variant2_id = variant2_response.json()["id"]

        # List variants - should have both
        list_response = api_client.get(f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}")
        assert list_response.status_code == 200
        variants = list_response.json()
        assert len(variants) == 2

        variant_ids = {v["id"] for v in variants}
        assert variant1_id in variant_ids
        assert variant2_id in variant_ids

        # Update first variant
        update_response = api_client.patch(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant1_id}",
            json={"title": "Updated First Variant"},
        )
        assert update_response.status_code == 200

        # Delete second variant
        delete_response = api_client.delete(
            f"/api/v1/variants/{sample_store['id']}/{sample_product['id']}/{variant2_id}"
        )
        assert delete_response.status_code == 204
