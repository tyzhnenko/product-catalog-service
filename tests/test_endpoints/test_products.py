# ruff: noqa: S101, D100, D101, D102, D103
import uuid

import pytest


@pytest.fixture
def sample_store(api_client):
    """Create a sample store for testing products."""
    store_data = {
        "name": "Test Store for Products",
        "url": "https://teststoreproducts.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def another_store(api_client):
    """Create another store for testing products."""
    store_data = {
        "name": "Another Product Store",
        "url": "https://anotherproductstore.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def sample_category(api_client, sample_store):
    """Create a sample category for testing products."""
    category_data = {
        "name": "Coffee Beans",
        "description": "All types of coffee beans",
        "status": "active",
        "path": "/coffee-beans",
    }
    response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
    return response.json()


@pytest.fixture
def another_category(api_client, sample_store):
    """Create another category for testing products."""
    category_data = {
        "name": "Light Roast",
        "description": "Light roasted coffee",
        "status": "active",
        "path": "/light-roast",
    }
    response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
    return response.json()


@pytest.fixture
def sample_product_data(sample_category):
    """Sample data for creating a product."""
    return {
        "name": "Ethiopian Yirgacheffe",
        "description": "A bright and fruity coffee from Ethiopia",
        "brand": "Origin Coffee",
        "tags": ["single-origin", "light-roast", "fruity"],
        "categories": [sample_category["id"]],
        "seo": {
            "slug": "ethiopian-yirgacheffe",
            "title": "Ethiopian Yirgacheffe Coffee - Light Roast",
            "description": (
                "Discover the bright and fruity flavors of "
                "Ethiopian Yirgacheffe coffee, expertly roasted to perfection."
            ),
            "keywords": "ethiopian coffee, yirgacheffe, light roast, single origin",
        },
    }


@pytest.fixture
def another_product_data(another_category):
    """Another sample product data for testing multiple products."""
    return {
        "name": "Colombian Supremo",
        "description": "Smooth and balanced coffee from Colombia",
        "brand": "Mountain Coffee",
        "tags": ["single-origin", "medium-roast"],
        "categories": [another_category["id"]],
        "seo": {
            "slug": "colombian-supremo",
            "title": "Colombian Supremo Coffee - Medium Roast",
            "keywords": "colombian coffee, supremo, medium roast",
            "description": (
                "Experience the smooth and balanced flavors of Colombian Supremo coffee, perfect for any time of day."
            ),
        },
    }


@pytest.fixture
def minimal_product_data():
    """Minimal product data with only required fields."""
    return {
        "name": "Simple Coffee",
        "tags": [],
        "categories": [],
    }


class TestCreateProduct:
    """Tests for POST /api/v1/products/{store_id}."""

    def test_create_product_success(self, api_client, sample_product_data, sample_store):
        """Test successful product creation."""
        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == sample_product_data["name"]
        assert data["description"] == sample_product_data["description"]
        assert data["tags"] == sample_product_data["tags"]
        assert data["categories"] == sample_product_data["categories"]
        assert data["seo"]["slug"] == sample_product_data["seo"]["slug"]
        assert data["status"] == "active"
        assert "id" in data
        # Validate UUID7 format
        assert uuid.UUID(data["id"]).version == 7

    def test_create_product_minimal_fields(self, api_client, minimal_product_data, sample_store):
        """Test product creation with minimal required fields."""
        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=minimal_product_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == minimal_product_data["name"]
        assert data["tags"] == []
        assert data["categories"] == []
        assert data["status"] == "active"
        assert "id" in data

    def test_create_product_missing_name(self, api_client, sample_store):
        """Test product creation without name."""
        invalid_data = {
            "tags": [],
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_product_empty_name(self, api_client, sample_store):
        """Test product creation with empty name."""
        invalid_data = {
            "name": "",
            "tags": [],
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_product_invalid_store_id(self, api_client, sample_product_data):
        """Test product creation with invalid store_id UUID format."""
        response = api_client.post("/api/v1/products/not-a-valid-uuid", json=sample_product_data)

        assert response.status_code == 422

    def test_create_product_nonexistent_store(self, api_client, sample_product_data):
        """Test product creation with non-existent store."""
        non_existent_store_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.post(f"/api/v1/products/{non_existent_store_id}", json=sample_product_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_create_product_name_too_long(self, api_client, sample_store):
        """Test product creation with name exceeding max length."""
        invalid_data = {
            "name": "A" * 513,  # Max is 512
            "tags": [],
            "categories": [],
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_product_with_invalid_category(self, api_client, sample_store):
        """Test product creation with non-existent category - should filter it out."""
        invalid_data = {
            "name": "Test Product",
            "tags": [],
            "categories": ["01939d8e-1234-7890-abcd-ef0123456789"],  # Non-existent category
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid category should be filtered out
        assert data["categories"] == []

    def test_create_product_with_category_from_different_store(self, api_client, sample_store, another_store):
        """Test product creation with category from a different store - should filter it out."""
        # Create category in another store
        category_data = {
            "name": "Other Store Category",
            "description": "Category in different store",
            "status": "active",
            "path": "/other",
            "paths": ["/other"],
        }
        category_response = api_client.post(f"/api/v1/categories/{another_store['id']}", json=category_data)
        category = category_response.json()

        # Try to create product in sample_store with category from another_store
        invalid_data = {
            "name": "Test Product",
            "tags": [],
            "categories": [category["id"]],
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 200
        data = response.json()
        # Category from different store should be filtered out
        assert data["categories"] == []

    def test_create_product_with_multiple_categories(self, api_client, sample_store, sample_category, another_category):
        """Test product creation with multiple categories."""
        product_data = {
            "name": "Multi-Category Product",
            "tags": [],
            "categories": [sample_category["id"], another_category["id"]],
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 2
        assert sample_category["id"] in data["categories"]
        assert another_category["id"] in data["categories"]

    def test_create_product_with_mixed_valid_invalid_categories(self, api_client, sample_store, sample_category):
        """Test product creation with mix of valid and invalid categories - keeps only valid ones."""
        product_data = {
            "name": "Mixed Categories Product",
            "tags": [],
            "categories": [
                sample_category["id"],
                "01939d8e-1234-7890-abcd-ef0123456789",  # Invalid
                "01939d8e-5678-7890-abcd-ef0123456789",  # Invalid
            ],
        }

        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)

        assert response.status_code == 200
        data = response.json()
        # Only the valid category should be kept
        assert len(data["categories"]) == 1
        assert data["categories"][0] == sample_category["id"]


class TestListProducts:
    """Tests for GET /api/v1/products/{store_id}."""

    def test_list_products_empty(self, api_client, sample_store):
        """Test listing products when database is empty."""
        response = api_client.get(f"/api/v1/products/{sample_store['id']}")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_products_with_one_product(self, api_client, sample_product_data, sample_store):
        """Test listing products with one product in database."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        created_product = create_response.json()

        # List products
        response = api_client.get(f"/api/v1/products/{sample_store['id']}")

        assert response.status_code == 200
        products = response.json()
        assert len(products) == 1
        assert products[0]["id"] == created_product["id"]
        assert products[0]["name"] == sample_product_data["name"]

    def test_list_products_with_multiple_products(
        self, api_client, sample_product_data, another_product_data, sample_store
    ):
        """Test listing multiple products."""
        # Create two products
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=another_product_data)

        # List products
        response = api_client.get(f"/api/v1/products/{sample_store['id']}")

        assert response.status_code == 200
        products = response.json()
        assert len(products) == 2

        product_names = {product["name"] for product in products}
        assert sample_product_data["name"] in product_names
        assert another_product_data["name"] in product_names

    def test_list_products_different_stores(self, api_client, sample_product_data, sample_store, another_store):
        """Test that products from different stores are isolated."""
        # Create product in first store
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)

        # List products from second store
        response = api_client.get(f"/api/v1/products/{another_store['id']}")

        assert response.status_code == 200
        products = response.json()
        assert len(products) == 0

    def test_list_products_nonexistent_store(self, api_client):
        """Test listing products for non-existent store."""
        non_existent_store_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/products/{non_existent_store_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"


class TestGetProduct:
    """Tests for GET /api/v1/products/{store_id}/{product_id}."""

    def test_get_product_success(self, api_client, sample_product_data, sample_store):
        """Test successful retrieval of a specific product."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        created_product = create_response.json()
        product_id = created_product["id"]

        # Get the product
        response = api_client.get(f"/api/v1/products/{sample_store['id']}/{product_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == sample_product_data["name"]
        assert data["description"] == sample_product_data["description"]

    def test_get_product_not_found(self, api_client, sample_store):
        """Test getting a non-existent product."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.get(f"/api/v1/products/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_get_product_wrong_store(self, api_client, sample_product_data, sample_store, another_store):
        """Test getting a product from wrong store."""
        # Create product in first store
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Try to get from second store
        response = api_client.get(f"/api/v1/products/{another_store['id']}/{product_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_get_product_invalid_uuid(self, api_client, sample_store):
        """Test getting a product with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/products/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422


class TestUpdateProduct:
    """Tests for PUT /api/v1/products/{store_id}/{product_id}."""

    def test_update_product_name(self, api_client, sample_product_data, sample_store):
        """Test updating product name."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Update the product name
        update_data = {"name": "Updated Coffee Name"}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Updated Coffee Name"
        assert data["description"] == sample_product_data["description"]  # Should remain unchanged

    def test_update_product_description(self, api_client, sample_product_data, sample_store):
        """Test updating product description."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Update the description
        update_data = {"description": "A completely new description"}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "A completely new description"

    def test_update_product_status(self, api_client, sample_product_data, sample_store):
        """Test updating product status."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Update status to archived
        update_data = {"status": "archived"}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "archived"

    def test_update_product_tags(self, api_client, sample_product_data, sample_store):
        """Test updating product tags."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Update tags
        update_data = {"tags": ["new-tag", "updated"]}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["tags"] == ["new-tag", "updated"]

    def test_update_product_categories(self, api_client, sample_product_data, sample_store, another_category):
        """Test updating product categories."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Update categories
        update_data = {"categories": [another_category["id"]]}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["categories"] == [another_category["id"]]

    def test_update_product_add_category(
        self, api_client, sample_product_data, sample_store, sample_category, another_category
    ):
        """Test adding a category to product."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Add another category
        update_data = {"categories": [sample_category["id"], another_category["id"]]}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 2
        assert sample_category["id"] in data["categories"]
        assert another_category["id"] in data["categories"]

    def test_update_product_remove_all_categories(self, api_client, sample_product_data, sample_store):
        """Test removing all categories from product."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Remove all categories
        update_data = {"categories": []}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["categories"] == []

    def test_update_product_with_invalid_category(self, api_client, sample_product_data, sample_store):
        """Test updating product with non-existent category - should filter it out."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Try to update with invalid category
        update_data = {"categories": ["01939d8e-1234-7890-abcd-ef0123456789"]}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid category should be filtered out
        assert data["categories"] == []

    def test_update_product_not_found(self, api_client, sample_store):
        """Test updating a non-existent product."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        update_data = {"name": "Updated Name"}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{non_existent_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_update_product_wrong_store(self, api_client, sample_product_data, sample_store, another_store):
        """Test updating a product from wrong store."""
        # Create product in first store
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Try to update from second store
        update_data = {"name": "Hacked Name"}
        response = api_client.patch(f"/api/v1/products/{another_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"


class TestDeleteProduct:
    """Tests for DELETE /api/v1/products/{store_id}/{product_id}."""

    def test_delete_product_success(self, api_client, sample_product_data, sample_store):
        """Test successful soft delete of a product."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Delete the product
        response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{product_id}")

        assert response.status_code == 204

    def test_delete_product_not_found(self, api_client, sample_store):
        """Test deleting a non-existent product."""
        non_existent_id = "01939d8e-1234-7890-abcd-ef0123456789"

        response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_delete_product_wrong_store(self, api_client, sample_product_data, sample_store, another_store):
        """Test deleting a product from wrong store."""
        # Create product in first store
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Try to delete from second store
        response = api_client.delete(f"/api/v1/products/{another_store['id']}/{product_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_delete_product_invalid_uuid(self, api_client, sample_store):
        """Test deleting a product with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422


class TestProductCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, api_client, sample_product_data, sample_store):
        """Test the complete CRUD lifecycle of a product."""
        # Create
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        assert create_response.status_code == 200
        created_product = create_response.json()
        product_id = created_product["id"]

        # Read (single)
        get_response = api_client.get(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == product_id

        # Read (list)
        list_response = api_client.get(f"/api/v1/products/{sample_store['id']}")
        assert list_response.status_code == 200
        assert len(list_response.json()) >= 1

        # Update
        update_data = {
            "name": "Updated Product Name",
            "status": "draft",
        }
        update_response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Product Name"
        assert update_response.json()["status"] == "draft"

        # Verify update
        get_updated_response = api_client.get(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["name"] == "Updated Product Name"

        # Delete
        delete_response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        get_deleted_response = api_client.get(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert get_deleted_response.status_code == 404
