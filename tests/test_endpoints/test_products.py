# ruff: noqa: S101, D100, D101, D102, D103
import pytest
from beanie import PydanticObjectId


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
        "attributes": {
            "roast_level": {"type": "string", "name": "roast_level", "value": "light"},
            "weight_grams": {"type": "integer", "name": "weight_grams", "value": 250},
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
        "attributes": {
            "roast_level": {"type": "string", "name": "roast_level", "value": "medium"},
            "organic": {"type": "bool", "name": "organic", "value": True},
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
        assert data["attributes"] == sample_product_data["attributes"]
        assert "id" in data

    def test_create_product_minimal_fields(self, api_client, minimal_product_data, sample_store):
        """Test product creation with minimal required fields."""
        response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=minimal_product_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == minimal_product_data["name"]
        assert data["tags"] == []
        assert data["categories"] == []
        assert data["status"] == "active"
        assert data["attributes"] == {}
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
        non_existent_store_id = str(PydanticObjectId())

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
            "categories": [str(PydanticObjectId())],  # Non-existent category
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
                str(PydanticObjectId()),  # Invalid
                str(PydanticObjectId()),  # Invalid
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
        assert response.json()["items"] == []

    def test_list_products_with_one_product(self, api_client, sample_product_data, sample_store):
        """Test listing products with one product in database."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        created_product = create_response.json()

        # List products
        response = api_client.get(f"/api/v1/products/{sample_store['id']}")

        assert response.status_code == 200
        products = response.json()["items"]
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
        products = response.json()["items"]
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
        products = response.json()["items"]
        assert len(products) == 0

    def test_list_products_nonexistent_store(self, api_client):
        """Test listing products for non-existent store."""
        non_existent_store_id = str(PydanticObjectId())

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
        non_existent_id = str(PydanticObjectId())

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

    def test_update_product_attributes(self, api_client, sample_product_data, sample_store):
        """Test updating product attributes."""
        # Create a product first
        create_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        product_id = create_response.json()["id"]

        # Update attributes
        update_data = {
            "attributes": {
                "roast_level": {"type": "string", "name": "roast_level", "value": "dark"},
                "fair_trade": {"type": "bool", "name": "fair_trade", "value": True},
            }
        }
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["attributes"]["roast_level"]["value"] == "dark"
        assert data["attributes"]["fair_trade"]["value"] is True
        assert "weight_grams" not in data["attributes"]  # Original attribute should be replaced

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
        update_data = {"categories": [str(PydanticObjectId())]}
        response = api_client.patch(f"/api/v1/products/{sample_store['id']}/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        # Invalid category should be filtered out
        assert data["categories"] == []

    def test_update_product_not_found(self, api_client, sample_store):
        """Test updating a non-existent product."""
        non_existent_id = str(PydanticObjectId())

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
        non_existent_id = str(PydanticObjectId())

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
        assert len(list_response.json()["items"]) >= 1

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


class TestProductRecursiveDelete:
    """Tests for recursive soft delete when deleting a product."""

    def test_delete_product_cascades_to_variants(self, api_client, sample_store):
        """Test that deleting a product soft deletes all its variants."""
        # Create a product
        product_data = {"name": "Product with Variants", "tags": []}
        product_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
        product_id = product_response.json()["id"]

        # Create multiple variants
        variant1_data = {"title": "Small", "options": [{"name": "size", "value": "small"}]}
        variant1_response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{product_id}", json=variant1_data)
        variant1_id = variant1_response.json()["id"]

        variant2_data = {"title": "Medium", "options": [{"name": "size", "value": "medium"}]}
        variant2_response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{product_id}", json=variant2_data)
        variant2_id = variant2_response.json()["id"]

        variant3_data = {"title": "Large", "options": [{"name": "size", "value": "large"}]}
        variant3_response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{product_id}", json=variant3_data)
        variant3_id = variant3_response.json()["id"]

        # Verify variants exist before deletion
        variants_list = api_client.get(f"/api/v1/variants/{sample_store['id']}/{product_id}")
        assert variants_list.status_code == 200
        assert len(variants_list.json()["items"]) == 3

        # Delete the product
        delete_response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert delete_response.status_code == 204

        # Verify all variants are soft deleted (not accessible)
        variant1_get = api_client.get(f"/api/v1/variants/{sample_store['id']}/{product_id}/{variant1_id}")
        variant2_get = api_client.get(f"/api/v1/variants/{sample_store['id']}/{product_id}/{variant2_id}")
        variant3_get = api_client.get(f"/api/v1/variants/{sample_store['id']}/{product_id}/{variant3_id}")

        assert variant1_get.status_code == 404
        assert variant2_get.status_code == 404
        assert variant3_get.status_code == 404

        # Verify the variants list is empty or returns 404
        variants_list_after = api_client.get(f"/api/v1/variants/{sample_store['id']}/{product_id}")
        assert variants_list_after.status_code in [404, 200]
        if variants_list_after.status_code == 200:
            assert len(variants_list_after.json()["items"]) == 0

    def test_delete_product_with_no_variants(self, api_client, sample_store):
        """Test that deleting a product with no variants works correctly."""
        # Create a product without variants
        product_data = {"name": "Product without Variants", "tags": []}
        product_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product_data)
        product_id = product_response.json()["id"]

        # Delete the product
        delete_response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert delete_response.status_code == 204

        # Verify product is deleted
        product_get = api_client.get(f"/api/v1/products/{sample_store['id']}/{product_id}")
        assert product_get.status_code == 404

    def test_delete_product_multiple_with_variants(self, api_client, sample_store):
        """Test deleting multiple products each with their own variants."""
        # Create first product with variants
        product1_data = {"name": "Product 1", "tags": []}
        product1_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product1_data)
        product1_id = product1_response.json()["id"]

        variant1_data = {"title": "Product 1 Variant", "options": [{"name": "color", "value": "red"}]}
        api_client.post(f"/api/v1/variants/{sample_store['id']}/{product1_id}", json=variant1_data)

        # Create second product with variants
        product2_data = {"name": "Product 2", "tags": []}
        product2_response = api_client.post(f"/api/v1/products/{sample_store['id']}", json=product2_data)
        product2_id = product2_response.json()["id"]

        variant2_data = {"title": "Product 2 Variant", "options": [{"name": "color", "value": "blue"}]}
        variant2_response = api_client.post(f"/api/v1/variants/{sample_store['id']}/{product2_id}", json=variant2_data)
        variant2_id = variant2_response.json()["id"]

        # Delete first product
        delete1_response = api_client.delete(f"/api/v1/products/{sample_store['id']}/{product1_id}")
        assert delete1_response.status_code == 204

        # Verify first product is deleted but second product and its variant still exist
        product1_get = api_client.get(f"/api/v1/products/{sample_store['id']}/{product1_id}")
        assert product1_get.status_code == 404

        product2_get = api_client.get(f"/api/v1/products/{sample_store['id']}/{product2_id}")
        assert product2_get.status_code == 200

        variant2_get = api_client.get(f"/api/v1/variants/{sample_store['id']}/{product2_id}/{variant2_id}")
        assert variant2_get.status_code == 200


class TestListProductsPagination:
    """Pagination tests for GET /api/v1/products/{store_id}."""

    def test_first_page_no_cursor(self, api_client, sample_store):
        """No cursor: first page, has_next when more items exist."""
        for i in range(3):
            api_client.post(f"/api/v1/products/{sample_store['id']}", json={"name": f"Product {i}", "tags": []})

        response = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 2})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["has_next"] is True
        assert data["has_prev"] is False
        assert data["end_cursor"] is not None

    def test_forward_pagination(self, api_client, sample_store):
        """after=end_cursor fetches the next page."""
        for i in range(3):
            api_client.post(f"/api/v1/products/{sample_store['id']}", json={"name": f"Product {i}", "tags": []})

        page1 = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 2}).json()
        end_cursor = page1["end_cursor"]

        page2_resp = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"after": end_cursor, "limit": 2})
        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 1
        assert page2["has_next"] is False
        assert page2["has_prev"] is True

    def test_middle_page_has_next(self, api_client, sample_store):
        """after=end_cursor on a middle page returns has_next=True and truncates to limit."""
        for i in range(5):
            api_client.post(f"/api/v1/products/{sample_store['id']}", json={"name": f"ProdMid {i}", "tags": []})

        page1 = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 2}).json()
        page2_resp = api_client.get(
            f"/api/v1/products/{sample_store['id']}", params={"after": page1["end_cursor"], "limit": 2}
        )

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 2
        assert page2["has_next"] is True
        assert page2["has_prev"] is True

    def test_middle_page_has_prev(self, api_client, sample_store):
        """before=start_cursor on a middle page returns has_prev=True and truncates to limit."""
        for i in range(5):
            api_client.post(f"/api/v1/products/{sample_store['id']}", json={"name": f"ProdPrev {i}", "tags": []})

        page1 = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 2}).json()
        page2 = api_client.get(
            f"/api/v1/products/{sample_store['id']}", params={"after": page1["end_cursor"], "limit": 2}
        ).json()
        page3 = api_client.get(
            f"/api/v1/products/{sample_store['id']}", params={"after": page2["end_cursor"], "limit": 2}
        ).json()

        back_resp = api_client.get(
            f"/api/v1/products/{sample_store['id']}", params={"before": page3["start_cursor"], "limit": 2}
        )

        assert back_resp.status_code == 200
        back = back_resp.json()
        assert len(back["items"]) == 2
        assert back["has_prev"] is True
        assert back["has_next"] is True

    def test_backward_pagination(self, api_client, sample_store):
        """before=start_cursor of page 2 returns page 1."""
        ids = []
        for i in range(3):
            r = api_client.post(f"/api/v1/products/{sample_store['id']}", json={"name": f"Product {i}", "tags": []})
            ids.append(r.json()["id"])

        page1 = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 2}).json()
        page2 = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params={"after": page1["end_cursor"], "limit": 2},
        ).json()

        back = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params={"before": page2["start_cursor"], "limit": 2},
        ).json()
        assert [item["id"] for item in back["items"]] == [item["id"] for item in page1["items"]]

    def test_empty_result(self, api_client, sample_store):
        """No products: empty paginated response."""
        response = api_client.get(f"/api/v1/products/{sample_store['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["start_cursor"] is None
        assert data["end_cursor"] is None
        assert data["has_next"] is False
        assert data["has_prev"] is False

    def test_invalid_cursor(self, api_client, sample_store):
        """Invalid cursor returns 400."""
        response = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"after": "not-a-valid-cursor"})
        assert response.status_code == 400

    def test_custom_limit(self, api_client, sample_store):
        """Limit query param is respected."""
        for i in range(5):
            api_client.post(f"/api/v1/products/{sample_store['id']}", json={"name": f"Product {i}", "tags": []})

        response = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 2})

        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
        assert response.json()["has_next"] is True

    def test_limit_max_enforced(self, api_client, sample_store):
        """Limit > max_limit returns 422."""
        response = api_client.get(f"/api/v1/products/{sample_store['id']}", params={"limit": 999})
        assert response.status_code == 422


class TestListProductsByAttributes:
    """Tests for GET /api/v1/products/{store_id}?attrs= filtering."""

    def test_filter_by_attribute_match(self, api_client, sample_product_data, another_product_data, sample_store):
        """Filter returns only products matching the attribute value."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=another_product_data)

        response = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params={"attrs": "roast_level:light"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["attributes"]["roast_level"]["value"] == "light"

    def test_filter_by_attribute_no_match(self, api_client, sample_product_data, sample_store):
        """Filter returns empty list when no products match."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)

        response = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params={"attrs": "roast_level:dark"},
        )

        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_filter_by_multiple_attributes_and(
        self, api_client, sample_product_data, another_product_data, sample_store
    ):
        """Multiple different-key attrs are ANDed together."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=another_product_data)

        # another_product_data has roast_level=medium AND organic=True
        response = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params=[("attrs", "roast_level:medium"), ("attrs", "organic:true")],
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["attributes"]["roast_level"]["value"] == "medium"

    def test_filter_by_same_key_multiple_values_or(
        self, api_client, sample_product_data, another_product_data, sample_store
    ):
        """Same-key attrs with multiple values are ORed via $in."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=another_product_data)

        response = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params=[("attrs", "roast_level:light"), ("attrs", "roast_level:medium")],
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 2

    def test_filter_by_integer_attribute(self, api_client, sample_product_data, another_product_data, sample_store):
        """Integer attribute values are coerced and matched correctly."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=another_product_data)

        response = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params={"attrs": "weight_grams:250"},
        )

        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["attributes"]["weight_grams"]["value"] == 250

    def test_filter_malformed_attrs_ignored(self, api_client, sample_product_data, sample_store):
        """Attrs entries without a colon are silently ignored (no filter applied)."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)

        response = api_client.get(
            f"/api/v1/products/{sample_store['id']}",
            params={"attrs": "no-colon-here"},
        )

        assert response.status_code == 200
        assert len(response.json()["items"]) == 1

    def test_empty_attrs_returns_all(self, api_client, sample_product_data, another_product_data, sample_store):
        """Empty attrs list applies no filter and returns all products."""
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=sample_product_data)
        api_client.post(f"/api/v1/products/{sample_store['id']}", json=another_product_data)

        response = api_client.get(f"/api/v1/products/{sample_store['id']}")

        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
