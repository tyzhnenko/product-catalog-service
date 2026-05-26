# ruff: noqa: S101, D100, D101, D102, D103
import pytest
from beanie import PydanticObjectId


@pytest.fixture
def sample_store(api_client):
    """Create a sample store for testing categories."""
    store_data = {
        "name": "Test Store for Categories",
        "url": "https://teststorecategories.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def another_store(api_client):
    """Create another store for testing categories."""
    store_data = {
        "name": "Another Test Store",
        "url": "https://anotherstore.com/",
    }
    response = api_client.post("/api/v1/stores/", json=store_data)
    return response.json()


@pytest.fixture
def sample_category_data(sample_store):
    """Sample data for creating a category."""
    return {
        "name": "Electronics",
        "description": "Electronic devices and accessories",
        "status": "active",
        "path": "/electronics",
        "seo": {
            "slug": "electronics",
            "title": "Electronics | Test Store",
            "description": "Shop the latest electronics and accessories",
            "keywords": "electronics, gadgets, devices",
            "path": "/electronics",
        },
        "attributes": {
            "brand": {
                "type": "string",
                "name": "brand",
                "value": "Generic",
            },
        },
    }


@pytest.fixture
def another_category_data(sample_store):
    """Another sample category data for testing multiple categories."""
    return {
        "name": "Laptops",
        "description": "Portable computers",
        "status": "active",
        "path": "/electronics/laptops",
        "seo": {
            "slug": "laptops",
            "title": "Laptops | Test Store",
            "description": "Shop the best laptops",
            "keywords": "laptops, computers, portable",
            "path": "/electronics/laptops",
        },
    }


class TestCreateCategory:
    """Tests for POST /api/v1/categories/{store_id}."""

    def test_create_category_success(self, api_client, sample_category_data, sample_store):
        """Test successful category creation."""
        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == sample_category_data["name"]
        assert data["description"] == sample_category_data["description"]
        assert data["status"] == sample_category_data["status"]
        assert data["path"] == sample_category_data["path"]
        assert data["seo"]["slug"] == sample_category_data["seo"]["slug"]
        assert "id" in data

    def test_create_category_minimal(self, api_client, sample_store):
        """Test creating category with minimal required fields."""
        minimal_data = {
            "name": "Test Category",
            "path": "/test-category",
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=minimal_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Category"
        assert data["status"] == "active"  # Default value
        assert data["path"] == "/test-category"
        assert "id" in data

    def test_create_category_missing_name(self, api_client, sample_store):
        """Test category creation without name."""
        invalid_data = {}

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_category_empty_name(self, api_client, sample_store):
        """Test category creation with empty name."""
        invalid_data = {
            "name": "",
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=invalid_data)

        assert response.status_code == 422

    def test_create_category_invalid_store_id(self, api_client):
        """Test category creation with invalid store_id UUID format."""
        invalid_data = {
            "name": "Test Category",
        }

        response = api_client.post("/api/v1/categories/not-a-valid-uuid", json=invalid_data)

        assert response.status_code == 422

    def test_create_category_nonexistent_store(self, api_client):
        """Test category creation with non-existent store."""
        non_existent_store_id = str(PydanticObjectId())
        invalid_data = {
            "name": "Test Category",
            "path": "/test-category",
        }

        response = api_client.post(f"/api/v1/categories/{non_existent_store_id}", json=invalid_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Store not found"

    def test_create_category_with_attributes(self, api_client, sample_store):
        """Test creating category with various attribute types."""
        category_data = {
            "name": "Tech Products",
            "path": "/tech-products",
            "attributes": {
                "warranty_years": {
                    "type": "integer",
                    "name": "warranty_years",
                    "value": 2,
                },
                "is_premium": {
                    "type": "bool",
                    "name": "is_premium",
                    "value": True,
                },
                "tags": {
                    "type": "list_of_strings",
                    "name": "tags",
                    "values": ["tech", "premium", "warranty"],
                },
            },
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 200
        data = response.json()
        assert "attributes" in data
        assert data["attributes"]["warranty_years"]["value"] == 2
        assert data["attributes"]["is_premium"]["value"] is True
        assert "tech" in data["attributes"]["tags"]["values"]


class TestListCategories:
    """Tests for GET /api/v1/categories/{store_id}."""

    def test_list_categories_empty(self, api_client, sample_store):
        """Test listing categories when database is empty."""
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}")

        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_list_categories_with_one_category(self, api_client, sample_category_data, sample_store):
        """Test listing categories with one category in database."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()

        # List categories
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}")

        assert response.status_code == 200
        categories = response.json()["items"]
        assert len(categories) == 1
        assert categories[0]["id"] == created_category["id"]
        assert categories[0]["name"] == sample_category_data["name"]

    def test_list_categories_with_multiple_categories(
        self, api_client, sample_category_data, another_category_data, sample_store
    ):
        """Test listing multiple categories."""
        # Create two categories
        api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        api_client.post(f"/api/v1/categories/{sample_store['id']}", json=another_category_data)

        # List categories
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}")

        assert response.status_code == 200
        categories = response.json()["items"]
        assert len(categories) == 2

        category_names = {category["name"] for category in categories}
        assert sample_category_data["name"] in category_names
        assert another_category_data["name"] in category_names

    def test_list_categories_excludes_deleted(self, api_client, sample_category_data, sample_store):
        """Test that listing categories excludes soft-deleted ones."""
        # Create a category
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Delete the category
        api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")

        # List categories - should be empty
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}")

        assert response.status_code == 200
        categories = response.json()["items"]
        assert len(categories) == 0


class TestGetCategory:
    """Tests for GET /api/v1/categories/{store_id}/{category_id}."""

    def test_get_category_success(self, api_client, sample_category_data, sample_store):
        """Test successful retrieval of a specific category."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Get the category
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{category_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == sample_category_data["name"]
        assert data["description"] == sample_category_data["description"]

    def test_get_category_not_found(self, api_client, sample_store):
        """Test getting a non-existent category."""
        non_existent_id = str(PydanticObjectId())

        response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"

    def test_get_category_invalid_uuid(self, api_client, sample_store):
        """Test getting a category with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422

    def test_get_deleted_category_not_found(self, api_client, sample_category_data, sample_store):
        """Test that getting a soft-deleted category returns 404."""
        # Create a category
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Delete the category
        api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")

        # Try to get the deleted category
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{category_id}")

        assert response.status_code == 404


class TestUpdateCategory:
    """Tests for PUT /api/v1/categories/{store_id}/{category_id}."""

    def test_update_category_name(self, api_client, sample_category_data, sample_store):
        """Test updating category name."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update the category name
        update_data = {
            "name": "Updated Category Name",
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == "Updated Category Name"
        assert data["description"] == sample_category_data["description"]  # Should remain unchanged

    def test_update_category_status(self, api_client, sample_category_data, sample_store):
        """Test updating category status."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update the category status
        update_data = {
            "status": "inactive",
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "inactive"

    def test_update_category_path(self, api_client, sample_category_data, sample_store):
        """Test updating category path."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update the category path
        update_data = {
            "path": "/electronics/computers",
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["path"] == "/electronics/computers"

    def test_update_category_seo(self, api_client, sample_category_data, sample_store):
        """Test updating category SEO information."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update the category SEO
        update_data = {
            "seo": {
                "slug": "updated-electronics",
                "title": "Updated Electronics | Test Store",
                "description": "Updated description",
                "keywords": "updated, keywords",
                "path": "/electronics",
            },
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["seo"]["slug"] == "updated-electronics"
        assert data["seo"]["title"] == "Updated Electronics | Test Store"

    def test_update_category_attributes(self, api_client, sample_category_data, sample_store):
        """Test updating category attributes."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update the category attributes
        update_data = {
            "attributes": {
                "new_attribute": {
                    "type": "string",
                    "name": "new_attribute",
                    "value": "new_value",
                },
            },
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert "new_attribute" in data["attributes"]
        assert data["attributes"]["new_attribute"]["value"] == "new_value"

    def test_update_category_multiple_fields(self, api_client, sample_category_data, sample_store):
        """Test updating multiple category fields at once."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update multiple fields
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description",
            "status": "inactive",
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated Description"
        assert data["status"] == "inactive"

    def test_update_category_not_found(self, api_client, sample_store):
        """Test updating a non-existent category."""
        non_existent_id = str(PydanticObjectId())

        update_data = {
            "name": "Updated Name",
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{non_existent_id}", json=update_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"

    def test_update_category_empty_name(self, api_client, sample_category_data, sample_store):
        """Test updating category with empty name."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Try to update with empty name
        update_data = {
            "name": "",
        }
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 422

    def test_update_deleted_category_not_found(self, api_client, sample_category_data, sample_store):
        """Test that updating a soft-deleted category returns 404."""
        # Create a category
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Delete the category
        api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")

        # Try to update the deleted category
        update_data = {"name": "Updated Name"}
        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)

        assert response.status_code == 404


class TestDeleteCategory:
    """Tests for DELETE /api/v1/categories/{store_id}/{category_id}."""

    def test_delete_category_success(self, api_client, sample_category_data, sample_store):
        """Test successful soft delete of a category."""
        # Create a category first
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Delete the category
        response = api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")

        assert response.status_code == 204

    def test_delete_category_not_found(self, api_client, sample_store):
        """Test deleting a non-existent category."""
        non_existent_id = str(PydanticObjectId())

        response = api_client.delete(f"/api/v1/categories/{sample_store['id']}/{non_existent_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"

    def test_delete_category_invalid_uuid(self, api_client, sample_store):
        """Test deleting a category with invalid UUID format."""
        invalid_id = "not-a-valid-uuid"

        response = api_client.delete(f"/api/v1/categories/{sample_store['id']}/{invalid_id}")

        assert response.status_code == 422

    def test_delete_already_deleted_category(self, api_client, sample_category_data, sample_store):
        """Test deleting an already deleted category."""
        # Create a category
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Delete the category
        first_delete = api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")
        assert first_delete.status_code == 204

        # Try to delete again
        second_delete = api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")
        assert second_delete.status_code == 404


class TestCategoryCRUDIntegration:
    """Integration tests for complete CRUD workflows."""

    def test_full_crud_lifecycle(self, api_client, sample_category_data, sample_store):
        """Test the complete CRUD lifecycle of a category."""
        # Create
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=sample_category_data)
        assert create_response.status_code == 200
        created_category = create_response.json()
        category_id = created_category["id"]

        # Read (single)
        get_response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{category_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == category_id

        # Read (list)
        list_response = api_client.get(f"/api/v1/categories/{sample_store['id']}")
        assert list_response.status_code == 200
        assert len(list_response.json()["items"]) >= 1

        # Update
        update_data = {
            "name": "Updated Category Name",
            "status": "inactive",
        }
        update_response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{category_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Category Name"
        assert update_response.json()["status"] == "inactive"

        # Verify update
        get_updated_response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{category_id}")
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["name"] == "Updated Category Name"

        # Delete
        delete_response = api_client.delete(f"/api/v1/categories/{sample_store['id']}/{category_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        get_deleted_response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{category_id}")
        assert get_deleted_response.status_code == 404

    def test_multiple_categories_for_same_store(self, api_client, sample_store):
        """Test creating multiple categories for the same store."""
        category1_data = {
            "name": "Category 1",
            "path": "/category1",
        }
        category2_data = {
            "name": "Category 2",
            "path": "/category2",
        }

        # Create two categories for the same store
        response1 = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category1_data)
        response2 = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category2_data)

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both have different category ids
        cat1 = response1.json()
        cat2 = response2.json()

        assert cat1["id"] != cat2["id"]
        assert cat1["name"] == "Category 1"
        assert cat2["name"] == "Category 2"

    def test_categories_across_different_stores(self, api_client, sample_store, another_store):
        """Test creating categories for different stores."""
        category1_data = {
            "name": "Store 1 Category",
            "path": "/store1-category",
        }
        category2_data = {
            "name": "Store 2 Category",
            "path": "/store2-category",
        }

        # Create categories for different stores
        response1 = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category1_data)
        response2 = api_client.post(f"/api/v1/categories/{another_store['id']}", json=category2_data)

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify they belong to different stores
        cat1 = response1.json()
        cat2 = response2.json()

        # List categories for store 1
        list_store1 = api_client.get(f"/api/v1/categories/{sample_store['id']}")
        assert len(list_store1.json()["items"]) == 1
        assert list_store1.json()["items"][0]["id"] == cat1["id"]

        # List categories for store 2
        list_store2 = api_client.get(f"/api/v1/categories/{another_store['id']}")
        assert len(list_store2.json()["items"]) == 1
        assert list_store2.json()["items"][0]["id"] == cat2["id"]

    def test_hierarchical_categories(self, api_client, sample_store):
        """Test creating hierarchical category structure."""
        parent_data = {
            "name": "Electronics",
            "path": "/electronics",
        }
        child_data = {
            "name": "Laptops",
            "path": "/electronics/laptops",
        }
        grandchild_data = {
            "name": "Gaming Laptops",
            "path": "/electronics/laptops/gaming",
        }

        # Create hierarchical categories
        parent_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=parent_data)
        child_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=child_data)
        grandchild_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=grandchild_data)

        assert parent_response.status_code == 200
        assert child_response.status_code == 200
        assert grandchild_response.status_code == 200

        # Verify paths
        parent = parent_response.json()
        child = child_response.json()
        grandchild = grandchild_response.json()

        assert parent["path"] == "/electronics"
        assert child["path"] == "/electronics/laptops"
        assert grandchild["path"] == "/electronics/laptops/gaming"


class TestCategoryImages:
    """Tests for category images field."""

    def test_create_category_with_single_image(self, api_client, sample_store):
        """Test creating a category with a single image."""
        category_data = {
            "name": "Electronics",
            "path": "/electronics",
            "images": [
                {
                    "url": "https://example.com/electronics.jpg",
                    "alt_text": "Electronics category banner",
                    "height": 1200,
                    "width": 1600,
                }
            ],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 200
        data = response.json()
        assert "images" in data
        assert data["images"] is not None
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/electronics.jpg"
        assert data["images"][0]["alt_text"] == "Electronics category banner"
        assert data["images"][0]["height"] == 1200
        assert data["images"][0]["width"] == 1600

    def test_create_category_with_multiple_images(self, api_client, sample_store):
        """Test creating a category with multiple images."""
        category_data = {
            "name": "Fashion",
            "path": "/fashion",
            "images": [
                {
                    "url": "https://example.com/fashion-banner.jpg",
                    "alt_text": "Fashion banner",
                },
                {
                    "url": "https://example.com/fashion-icon.png",
                    "alt_text": "Fashion icon",
                    "height": 256,
                    "width": 256,
                },
                {
                    "url": "https://example.com/fashion-promo.jpg",
                },
            ],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 3
        assert data["images"][0]["url"] == "https://example.com/fashion-banner.jpg"
        assert data["images"][1]["height"] == 256
        assert data["images"][2]["alt_text"] is None

    def test_create_category_with_image_attributes(self, api_client, sample_store):
        """Test creating a category with images that have custom attributes."""
        category_data = {
            "name": "Home & Garden",
            "path": "/home-garden",
            "images": [
                {
                    "url": "https://example.com/home.jpg",
                    "alt_text": "Home and garden category",
                    "attributes": {
                        "image_type": {
                            "type": "string",
                            "name": "image_type",
                            "value": "banner",
                        },
                        "display_order": {
                            "type": "integer",
                            "name": "display_order",
                            "value": 1,
                        },
                        "is_mobile_optimized": {
                            "type": "bool",
                            "name": "is_mobile_optimized",
                            "value": True,
                        },
                    },
                }
            ],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 1
        assert "attributes" in data["images"][0]
        assert data["images"][0]["attributes"]["image_type"]["value"] == "banner"
        assert data["images"][0]["attributes"]["display_order"]["value"] == 1
        assert data["images"][0]["attributes"]["is_mobile_optimized"]["value"] is True

    def test_create_category_without_images(self, api_client, sample_store):
        """Test that categories can be created without images (images is optional)."""
        category_data = {
            "name": "Books",
            "path": "/books",
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 200
        data = response.json()
        assert data["images"] is None

    def test_create_category_with_empty_images_list(self, api_client, sample_store):
        """Test creating a category with an empty images list."""
        category_data = {
            "name": "Sports",
            "path": "/sports",
            "images": [],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 200
        data = response.json()
        assert data["images"] == []

    def test_update_category_add_images(self, api_client, sample_store):
        """Test adding images to an existing category."""
        # Create category without images
        category_data = {
            "name": "Toys",
            "path": "/toys",
        }
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
        created_category = create_response.json()

        # Update category with images
        update_data = {
            "images": [
                {
                    "url": "https://example.com/toys-banner.jpg",
                    "alt_text": "Toys category",
                }
            ],
        }

        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{created_category['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/toys-banner.jpg"

    def test_update_category_modify_images(self, api_client, sample_store):
        """Test modifying existing images of a category."""
        # Create category with images
        category_data = {
            "name": "Beauty",
            "path": "/beauty",
            "images": [
                {
                    "url": "https://example.com/old-beauty.jpg",
                    "alt_text": "Old beauty image",
                }
            ],
        }
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
        created_category = create_response.json()

        # Update images
        update_data = {
            "images": [
                {
                    "url": "https://example.com/new-beauty1.jpg",
                    "alt_text": "New beauty image 1",
                },
                {
                    "url": "https://example.com/new-beauty2.jpg",
                    "alt_text": "New beauty image 2",
                },
            ],
        }

        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{created_category['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 2
        assert data["images"][0]["url"] == "https://example.com/new-beauty1.jpg"
        assert data["images"][1]["url"] == "https://example.com/new-beauty2.jpg"

    def test_update_category_remove_images(self, api_client, sample_store):
        """Test removing images from a category by setting to empty list."""
        # Create category with images
        category_data = {
            "name": "Automotive",
            "path": "/automotive",
            "images": [
                {
                    "url": "https://example.com/auto.jpg",
                }
            ],
        }
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
        created_category = create_response.json()

        # Remove images
        update_data = {"images": []}

        response = api_client.put(f"/api/v1/categories/{sample_store['id']}/{created_category['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["images"] == []

    def test_get_category_with_images(self, api_client, sample_store):
        """Test retrieving a category with images."""
        # Create category with images
        category_data = {
            "name": "Furniture",
            "path": "/furniture",
            "images": [
                {
                    "url": "https://example.com/furniture.jpg",
                    "alt_text": "Furniture category",
                    "height": 800,
                    "width": 1200,
                }
            ],
        }
        create_response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)
        created_category = create_response.json()

        # Retrieve category
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}/{created_category['id']}")

        assert response.status_code == 200
        data = response.json()
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/furniture.jpg"
        assert data["images"][0]["alt_text"] == "Furniture category"

    def test_list_categories_with_images(self, api_client, sample_store):
        """Test listing categories includes images."""
        # Create category with images
        category_data1 = {
            "name": "Category 1",
            "path": "/cat1",
            "images": [{"url": "https://example.com/cat1.jpg"}],
        }
        api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data1)

        # Create category without images
        category_data2 = {
            "name": "Category 2",
            "path": "/cat2",
        }
        api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data2)

        # List categories
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}")

        assert response.status_code == 200
        data = response.json()["items"]
        assert len(data) == 2

        # Find categories
        cat_with_images = next(c for c in data if c["name"] == "Category 1")
        cat_without_images = next(c for c in data if c["name"] == "Category 2")

        assert len(cat_with_images["images"]) == 1
        assert cat_without_images["images"] is None

    def test_create_category_invalid_image_url(self, api_client, sample_store):
        """Test that invalid image URLs are rejected."""
        category_data = {
            "name": "Invalid Image Category",
            "path": "/invalid",
            "images": [
                {
                    "url": "not-a-valid-url",
                    "alt_text": "Invalid",
                }
            ],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 422

    def test_create_category_image_with_zero_dimensions(self, api_client, sample_store):
        """Test that zero image dimensions are rejected."""
        category_data = {
            "name": "Zero Dimensions Category",
            "path": "/zero",
            "images": [
                {
                    "url": "https://example.com/image.jpg",
                    "height": 0,
                    "width": 500,
                }
            ],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 422

    def test_create_category_image_alt_text_empty(self, api_client, sample_store):
        """Test that empty alt_text is rejected."""
        category_data = {
            "name": "Empty Alt Text Category",
            "path": "/empty-alt",
            "images": [
                {
                    "url": "https://example.com/image.jpg",
                    "alt_text": "",
                }
            ],
        }

        response = api_client.post(f"/api/v1/categories/{sample_store['id']}", json=category_data)

        assert response.status_code == 422


class TestListCategoriesPagination:
    """Pagination tests for GET /api/v1/categories/{store_id}."""

    def test_first_page_no_cursor(self, api_client, sample_store):
        """No cursor: first page, has_next when more items exist."""
        for i in range(3):
            api_client.post(
                f"/api/v1/categories/{sample_store['id']}",
                json={"name": f"Category {i}", "path": f"/cat-{i}"},
            )

        response = api_client.get(f"/api/v1/categories/{sample_store['id']}", params={"limit": 2})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["has_next"] is True
        assert data["has_prev"] is False

    def test_forward_pagination(self, api_client, sample_store):
        """after=end_cursor fetches the next page."""
        for i in range(3):
            api_client.post(
                f"/api/v1/categories/{sample_store['id']}",
                json={"name": f"CatFwd {i}", "path": f"/catfwd-{i}"},
            )

        page1 = api_client.get(f"/api/v1/categories/{sample_store['id']}", params={"limit": 2}).json()
        page2_resp = api_client.get(
            f"/api/v1/categories/{sample_store['id']}", params={"after": page1["end_cursor"], "limit": 2}
        )

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 1
        assert page2["has_next"] is False
        assert page2["has_prev"] is True

    def test_middle_page_has_next(self, api_client, sample_store):
        """after=end_cursor on a middle page returns has_next=True and truncates to limit."""
        for i in range(5):
            api_client.post(
                f"/api/v1/categories/{sample_store['id']}",
                json={"name": f"CatMid {i}", "path": f"/catmid-{i}"},
            )

        page1 = api_client.get(f"/api/v1/categories/{sample_store['id']}", params={"limit": 2}).json()
        page2_resp = api_client.get(
            f"/api/v1/categories/{sample_store['id']}", params={"after": page1["end_cursor"], "limit": 2}
        )

        assert page2_resp.status_code == 200
        page2 = page2_resp.json()
        assert len(page2["items"]) == 2
        assert page2["has_next"] is True
        assert page2["has_prev"] is True

    def test_middle_page_has_prev(self, api_client, sample_store):
        """before=start_cursor on a middle page returns has_prev=True and truncates to limit."""
        for i in range(5):
            api_client.post(
                f"/api/v1/categories/{sample_store['id']}",
                json={"name": f"CatPrev {i}", "path": f"/catprev-{i}"},
            )

        page1 = api_client.get(f"/api/v1/categories/{sample_store['id']}", params={"limit": 2}).json()
        page2 = api_client.get(
            f"/api/v1/categories/{sample_store['id']}", params={"after": page1["end_cursor"], "limit": 2}
        ).json()
        page3 = api_client.get(
            f"/api/v1/categories/{sample_store['id']}", params={"after": page2["end_cursor"], "limit": 2}
        ).json()

        back_resp = api_client.get(
            f"/api/v1/categories/{sample_store['id']}", params={"before": page3["start_cursor"], "limit": 2}
        )

        assert back_resp.status_code == 200
        back = back_resp.json()
        assert len(back["items"]) == 2
        assert back["has_prev"] is True
        assert back["has_next"] is True

    def test_empty_result(self, api_client, sample_store):
        """No categories: empty paginated response."""
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["start_cursor"] is None
        assert data["end_cursor"] is None
        assert data["has_next"] is False
        assert data["has_prev"] is False

    def test_invalid_cursor(self, api_client, sample_store):
        """Invalid cursor returns 400."""
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}", params={"after": "not-a-valid-cursor"})
        assert response.status_code == 400

    def test_limit_max_enforced(self, api_client, sample_store):
        """Limit > max_limit returns 422."""
        response = api_client.get(f"/api/v1/categories/{sample_store['id']}", params={"limit": 999})
        assert response.status_code == 422
